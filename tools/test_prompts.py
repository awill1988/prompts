import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch
import zipfile

from fetch_model import download, extract_runner
from review_prompts import changed_documents, disposition, review_input, review, infer, CONTEXT_TOKENS
from validate_prompts import validate


class ValidationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.entry = self.root / 'instructions/AGENTS.md'
        self.entry.parent.mkdir()
        self.entry.write_text('# Policy\n\nUse explicit identities.\n')

    def test_valid_document(self):
        self.assertEqual(validate(self.root), ([], []))

    def test_missing_entrypoint(self):
        self.entry.unlink()
        self.assertTrue(validate(self.root)[0])

    def test_empty_document(self):
        self.entry.write_text(' ')
        self.assertTrue(validate(self.root)[0])

    def test_invalid_utf8(self):
        self.entry.write_bytes(b'\xff')
        self.assertTrue(validate(self.root)[0])

    def test_symlink_entrypoint(self):
        self.entry.rename(self.root / 'policy.md')
        self.entry.symlink_to('../policy.md')
        self.assertTrue(validate(self.root)[0])

    def test_broken_link(self):
        self.entry.write_text('[absent](missing.md)')
        self.assertTrue(validate(self.root)[0])

    def test_broken_fragment(self):
        self.entry.write_text('# Present\n\n[absent](#absent)')
        self.assertTrue(validate(self.root)[0])

    def test_literal_example_is_not_link(self):
        self.entry.write_text('`[example](absent.md)`\n')
        self.assertFalse(validate(self.root)[0])

    def test_scaffold(self):
        self.entry.write_text('TODO: complete policy')
        self.assertTrue(validate(self.root)[0])

    def test_size_is_advisory(self):
        self.entry.write_text('policy\n' * 501)
        errors, warnings = validate(self.root)
        self.assertFalse(errors)
        self.assertTrue(warnings)


class ReviewTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.git('init', '-q')
        self.git('config', 'user.name', 'Test')
        self.git('config', 'user.email', 'test@example.com')
        self.entry = self.root / 'instructions/AGENTS.md'
        self.entry.parent.mkdir()
        self.entry.write_text('# Policy\n\nRequire explicit identity.\n')
        self.commit()
        self.base = self.git('rev-parse', 'HEAD').strip()

    def git(self, *args):
        return subprocess.check_output(['git', *args], cwd=self.root, text=True, stderr=subprocess.DEVNULL)

    def commit(self):
        self.git('add', '.')
        self.git('-c', 'commit.gpgsign=false', 'commit', '-qm', 'test fixture')

    def test_no_change(self):
        self.assertEqual(changed_documents(self.root, self.base, 'HEAD'), [])

    def test_complete_document_and_diff(self):
        self.entry.write_text('# Policy\n\nRequire configured identity.\n')
        self.commit()
        prompt = review_input(self.root, self.base, 'HEAD', 'instructions/AGENTS.md')
        self.assertIn('Require configured identity.', prompt)
        self.assertIn('-Require explicit identity.', prompt)

    def test_delete_retains_old_document(self):
        self.entry.unlink()
        self.commit()
        prompt = review_input(self.root, self.base, 'HEAD', 'instructions/AGENTS.md')
        self.assertIn('complete deleted document', prompt)
        self.assertIn('Require explicit identity.', prompt)

    def test_rename_reviews_both_interfaces(self):
        self.entry.rename(self.entry.with_name('RULES.md'))
        self.commit()
        self.assertEqual(len(changed_documents(self.root, self.base, 'HEAD')), 2)

    def test_new_document(self):
        (self.entry.parent / 'other.md').write_text('# Other\n')
        self.commit()
        self.assertEqual(changed_documents(self.root, self.base, 'HEAD'), ['instructions/other.md'])

    def test_oversize_is_not_truncated(self):
        self.entry.write_text('x' * CONTEXT_TOKENS)
        self.commit()
        with self.assertRaises(ValueError):
            review_input(self.root, self.base, 'HEAD', 'instructions/AGENTS.md')

    def test_invalid_revision_fails(self):
        with self.assertRaises(subprocess.CalledProcessError):
            changed_documents(self.root, 'missing', 'HEAD')

    def test_terminal_disposition(self):
        self.assertEqual(disposition(json.dumps({'evidence': 'Require explicit identity.',
            'assessment': 'The policy retains an explicit identity boundary.', 'disposition': 'APPROVE'})), 'APPROVE')

    def test_malformed_disposition(self):
        for output in ['', 'approved', '{"disposition":"APPROVE"}',
                       '{"assessment":"fine","disposition":"PASS"}',
                       '{"assessment":"fine","disposition":"APPROVE"} trailing']:
            with self.subTest(output=output), self.assertRaises(ValueError):
                disposition(output)

    def test_missing_runner_cannot_approve(self):
        self.entry.write_text('# Revised\n')
        self.commit()
        with self.assertRaises(FileNotFoundError):
            review(self.root, self.base, 'HEAD', self.root/'model', self.root/'runner')

    def test_failed_inference_propagates(self):
        self.entry.write_text('# Revised\n')
        self.commit()
        with patch('review_prompts.infer', side_effect=RuntimeError('failed')):
            with self.assertRaises(RuntimeError):
                review(self.root, self.base, 'HEAD', None, None)

    def test_runner_transport_marker(self):
        output = '{"assessment":"No material defects.","disposition":"APPROVE"}'
        result = subprocess.CompletedProcess([], 0, output + ' [end of text]\n', '')
        with patch('review_prompts.subprocess.run', return_value=result):
            self.assertEqual(infer(Path('/model'), Path('/runner'), 'prompt'), output)

    def test_fabricated_evidence_cannot_approve(self):
        self.entry.write_text('# Revised\n\nRequire configured identity.\n')
        self.commit()
        response = json.dumps({'evidence': 'An instruction absent from the document.',
            'assessment': 'This fabricated instruction would be a material issue.', 'disposition': 'APPROVE'})
        with patch('review_prompts.infer', return_value=response), self.assertRaises(ValueError):
            review(self.root, self.base, 'HEAD', None, None)

    def test_grounded_assessment(self):
        self.entry.write_text('# Revised\n\nRequire configured identity.\n')
        self.commit()
        response = json.dumps({'evidence': 'Require configured identity.',
            'assessment': 'The change retains the configured identity boundary.', 'disposition': 'APPROVE'})
        with patch('review_prompts.infer', return_value=response):
            findings = review(self.root, self.base, 'HEAD', None, None)
        self.assertEqual(findings[0]['disposition'], 'APPROVE')


class DownloadTests(unittest.TestCase):
    def test_bad_checksum_preserves_existing_artifact(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source, target = root/'source', root/'target'
            source.write_bytes(b'bad')
            target.write_bytes(b'old')
            with self.assertRaises(RuntimeError):
                download([source.as_uri()], target, hashlib.sha256(b'good').hexdigest())
            self.assertEqual(target.read_bytes(), b'old')

    def test_verified_download(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source, target = root/'source', root/'target'
            source.write_bytes(b'good')
            download([source.as_uri()], target, hashlib.sha256(b'good').hexdigest())
            self.assertEqual(target.read_bytes(), b'good')

    def test_archive_escape(self):
        with tempfile.TemporaryDirectory() as directory:
            archive = Path(directory)/'runner.zip'
            with zipfile.ZipFile(archive, 'w') as bundle:
                bundle.writestr('../escaped', 'bad')
            with self.assertRaises(ValueError):
                extract_runner(archive, Path(directory)/'runner')


if __name__ == '__main__':
    unittest.main()
