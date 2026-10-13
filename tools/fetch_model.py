#!/usr/bin/env python3
"""Fetch pinned, verified model and runner artifacts for Linux CI."""

import argparse
import hashlib
import os
from pathlib import Path
import tempfile
import urllib.request
import zipfile

DOWNLOAD_CHUNK_BYTES = 1024 * 1024  # 1 MiB


def configuration(path):
    return dict(line.split("=", 1) for line in Path(path).read_text().splitlines()
                if line and not line.startswith("#"))


def checksum(path):
    with Path(path).open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def download(urls, target, digest):
    target = Path(target)
    if target.is_file() and checksum(target) == digest:
        return
    failures = []
    for url in urls:
        temporary = None
        try:
            with tempfile.NamedTemporaryFile(dir=target.parent, delete=False) as out:
                temporary = Path(out.name)
                with urllib.request.urlopen(url, timeout=60) as response:
                    while chunk := response.read(DOWNLOAD_CHUNK_BYTES):
                        out.write(chunk)
            if checksum(temporary) != digest:
                raise ValueError("checksum mismatch")
            os.replace(temporary, target)
            return
        except (OSError, ValueError) as error:
            failures.append(f"{url}: {error}")
        finally:
            if temporary is not None:
                temporary.unlink(missing_ok=True)
    raise RuntimeError("verified download failed: " + "; ".join(failures))


def extract_runner(archive, destination):
    destination = Path(destination).resolve()
    with zipfile.ZipFile(archive) as bundle:
        for entry in bundle.infolist():
            if not (destination / entry.filename).resolve().is_relative_to(destination):
                raise ValueError("runner archive path escapes destination")
        bundle.extractall(destination)
    runners = list(destination.rglob("llama-cli"))
    if len(runners) != 1:
        raise ValueError("expected exactly one llama-cli runner")
    runners[0].chmod(0o755)
    return runners[0]


def ensure(cache, config):
    cache.mkdir(parents=True, exist_ok=True)
    model = cache / config["MODEL_NAME"]
    download([config["PRIMARY_MODEL_URL"], config["FALLBACK_MODEL_URL"]], model,
             config["MODEL_SHA256"])
    archive = cache / "runner.zip"
    download([config["LLAMA_RUNNER_URL"]], archive, config["LLAMA_RUNNER_SHA256"])
    # Re-extract the verified archive so cached executables cannot bypass verification.
    runner = extract_runner(archive, cache / "runner")
    return model, runner


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cache-dir", type=Path, default=Path.home() / ".cache/prompt-review")
    args = parser.parse_args()
    ensure(args.cache_dir, configuration(Path(__file__).with_name("model.env")))
    print("model and runner verified")


if __name__ == "__main__":
    main()
