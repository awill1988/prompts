#!/usr/bin/env python3
"""Validate the distribution contract and repository Markdown references."""

import argparse
from pathlib import Path
import re
import sys

from markdown_validation import markdown_link_errors


def validate(root):
    root = Path(root).resolve()
    errors, warnings = [], []
    entrypoint = root / "instructions/AGENTS.md"
    if not entrypoint.is_file() or entrypoint.is_symlink():
        errors.append("instructions/AGENTS.md: expected a regular distribution file")
    for document in sorted(root.rglob("*.md")):
        if any(part.startswith(".") for part in document.relative_to(root).parts):
            continue
        label = str(document.relative_to(root))
        try:
            body = document.read_text(encoding="utf-8")
            if not body.strip():
                errors.append(f"{label}: empty document")
            if "\x00" in body:
                errors.append(f"{label}: unexpected nul byte")
            if re.search(r"\bTODO:\s*(complete|define|fill|replace)", body, re.I):
                errors.append(f"{label}: unfinished scaffold")
            errors.extend(f"{label}: {error}" for error in markdown_link_errors(body, document, root))
            if document == entrypoint and len(body.splitlines()) > 500:
                warnings.append(f"{label}: review size above 500 lines")
        except (UnicodeError, OSError) as error:
            errors.append(f"{label}: {error}")
    return errors, warnings


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    errors, warnings = validate(parser.parse_args().root)
    for warning in warnings:
        print(f"warning: {warning}", file=sys.stderr)
    for error in errors:
        print(f"error: {error}", file=sys.stderr)
    if not errors:
        print("prompt validation passed")
    return bool(errors)


if __name__ == "__main__":
    sys.exit(main())
