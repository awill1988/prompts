# prompts

Shared engineering instructions and technology policies. Every developer
profile receives the same instructions; the consuming configuration owns
identity routing, credentials, permissions, and installation.

## Distribution

[`instructions/AGENTS.md`](instructions/AGENTS.md) is the stable, self-contained
distribution interface. Client filenames are installation aliases, not separate
policies. The initial import preserves the current dotfiles policies while
clarifying contradictory SQL connector preflight instructions. The broader
redesign is reviewed independently.

Dotfiles consumes this public repository as a non-flake Nix input pinned in
`flake.lock`. Publishing here does not update an installed machine. See the
[ownership decision](docs/adr/0001-shared-instruction-ownership.md).

## Validation

```sh
uv run --with-requirements tools/requirements.txt python tools/validate_prompts.py
uv run --with-requirements tools/requirements.txt python -m unittest discover -s tools -p 'test_*.py'
```

`Prompt Validation` runs on every PR, including drafts. It checks the distribution
interface and Markdown references and runs the tooling tests.

`Prompt Model Review` runs on non-draft PRs and manual dispatch. It reviews full
document context and changes using a pinned local model and verified Linux
runner. Missing, failed, malformed, or oversized reviews fail the check.
Neither unit tests nor deterministic lint substitute for this assessment.
The model can make mistakes; inspect its findings and the underlying change.

Run the same review on Linux:

```sh
python tools/review_prompts.py --base origin/main --head HEAD
LOG_LEVEL=debug python tools/review_prompts.py --base origin/main --head HEAD
/usr/bin/time -v python tools/review_prompts.py --base origin/main --head HEAD
```

These are interpreted tools; there are no separate release/debug binaries.
`review.json` and `review.md` contain machine-readable and rendered results.
CI publishes these as artifacts and a job summary with read-only permissions.

## Contribution and publication

Use feature branches targeting `main`. Keep substantive policy changes visible
in the migration record. Both `prompt-validation` and `prompt-model-review` are
required checks; repository administrators configure that requirement separately
from the workflow definitions. Do not merge draft PRs with a skipped review.

Dotfiles updates its pinned input after the desired prompt revision is merged.
Its contract tests, build, activation, and rollback belong to that repository.
