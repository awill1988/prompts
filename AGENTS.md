# Repository instructions

Maintain `instructions/AGENTS.md` as the self-contained distribution interface.
All profiles and clients receive the same policy. Keep identity routing,
credentials, permissions, and installation in the consuming configuration.

Read `README.md` and the ownership ADR before changing the interface. Keep
policy changes separate from editorial changes in the migration record.
Run the validator and unit tests before committing. A lint-only result is not
a completed model review. Do not add automated contributor attribution to
commits, pull requests, or source metadata.

Use conventional commit subjects and the configured personal Git identity.
Verify the branch before plain `git push`; do not push directly to `main`.
