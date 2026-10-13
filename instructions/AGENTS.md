# Engineering instructions

These instructions apply to every developer profile. Apply technology rules
when that technology is involved. Read the target repository's instructions
and documentation before changing it.

## Authority and identity

- Treat repository `AGENTS.md` as the canonical instruction source;
  `CLAUDE.md` and `AGY.md` are compatibility shims when they delegate to it.
- Use the environment's configured developer profile, account, Git identity,
  and permitted tools. Respect repository and organizational authorization
  boundaries. Do not substitute another account or client to bypass them.
- Obtain identity and routing details from configuration rather than assuming
  them from a directory name or copying credentials between profiles.
- Never add automated-assistance attribution to commits, pull requests, code
  comments, release notes, changelogs, or contributor metadata. Verify commit
  and PR text before publication; omit attribution signatures and footers.

## Communication

- Lead with the action or technical outcome. Be concise, direct, and respectful.
  Avoid filler, pleasantries, project-management boilerplate, and curt remarks.
- Carry out settled decisions without editorial commentary. Ask only for
  information or authorization that is actually missing.
- Explain complexity through affected boundaries, invariants, and refactoring
  scope. Do not use task-duration estimates as a substitute for engineering
  reasoning. Mechanical properties such as measured runtime remain relevant.

## Implementation and verification

- Read existing files before editing. Use the available file-editing tools;
  preserve unrelated changes and validate inputs early.
- Prefer idiomatic `snake_case`, lowercase acronyms, and intention-revealing
  domain names. Keep log messages lowercase and use `LOG_LEVEL` for verbosity.
- Keep secrets out of source; obtain them through the configured secret or
  environment mechanism. Keep scripts and playbooks idempotent.
- Preserve architectural boundaries. Refactor fragile seams needed for the
  change rather than bypassing them to reduce implementation effort.
- Complete relevant tests, linting, and verification. Report unverified behavior
  explicitly; passing formatting or static checks does not prove runtime behavior.
- When adding developer commands, cover running, testing, debug/release modes
  where the toolchain supports them, and memory profiling where applicable.
  Use the `.vscode/tasks.json` schema for editor tasks.
- Comments explain intent, contracts, and rationale. Add a human-readable
  unit comment beside fixed binary sizes, such as `# 200 MiB`.
- Reference source locations with file paths and line numbers.

## Git

- Verify configured author and signing identities before committing.
- Use conventional subjects: `feat:`, `fix:`, `refactor:`, `chore:`, or `docs:`.
  Keep subjects within 50 characters and wrap bodies at 72 characters.
- When the branch contains a ticket, prefix the subject with `[TICKET-123]`.
  Keep conventional text lowercase after the ticket prefix in PR titles.
- Do not put commit hashes in commit messages or PR titles.
- PR descriptions state changed behavior, affected modules, verification, and
  manual steps. Do not add task lists unless requested.
- Before pushing, run `git branch --show-current`. Use plain `git push` so
  configured upstream safety checks remain effective; do not use refspecs to
  circumvent them.
- Do not push directly to `main` or `master` without explicit authorization.
  Never force-push protected or shared branches. If push refuses because of
  upstream mismatch, stop and ask rather than changing tracking to bypass it.

## AWS

- Before AWS CLI, SDK, or infrastructure operations, check `AWS_PROFILE` and
  `AWS_REGION`. If either is unset, obtain the target from the user before
  executing. Never assume a default account or region.
- Preserve the configured account boundary throughout the operation.

## SQL and Snowflake

- Execute SQL-capable tool calls sequentially. Wait for each query to complete
  before submitting another, including queries to different databases.
- Inspect connector capabilities before issuing database commands. Do not
  infer allowed statements from the database product alone.
- Before data queries, inspect an `EXPLAIN` plan. Use `EXPLAIN ANALYZE` only
  when executing the underlying query is already safe and authorized.
- Check index use or partition pruning as applicable. Refine queries that scan
  large tables; avoid unbounded aggregation, cross joins, and broad filters.
  Use selective predicates and `LIMIT` during exploration; `LIMIT` alone does
  not establish bounded scan cost.
- Metadata commands and session controls use their native syntax; do not wrap
  commands that cannot be explained in invalid `EXPLAIN` statements.
- For Snowflake, set `STATEMENT_TIMEOUT_IN_SECONDS` to `10` once per persistent
  session through an authorized session-control mechanism before data queries.
  Check partition pruning, including for `SNOWFLAKE.ACCOUNT_USAGE` queries.
- If required plan inspection or session setup is unavailable, report that
  missing capability and stop the dependent query. Do not invent successful
  preflight or bypass connector restrictions.
- Require explicit confirmation for `DROP`, `TRUNCATE`, and unfiltered `DELETE`
  or `UPDATE`. Filtered writes still require task authorization.

## Technical documentation and tools

- Read repository documentation for deployment commands, configuration paths,
  and gateway setup. Those details belong to the consuming environment.
- For library APIs, version-specific behavior, and framework debugging, consult
  current authoritative documentation. When Context7 is available, resolve the
  library identifier before querying its documentation.
- Write documentation in Markdown with coherent, terse headings. Wrap paths,
  commands, flags, configuration keys, resource names, and other developer
  literals in backticks. Escape Markdown-sensitive generated content.
- Describe discrepancies through the invariant, observed mismatch, and remedy
  without assigning blame.
- Track stale documentation found during implementation. Plan documentation
  updates separately for user review; do not silently include them as an
  implementation subtask. Approved documentation work can proceed within its
  agreed scope.

## Autonomous loops

- Resolve the workspace's configured profile and allowed tools before starting
  an autonomous loop. Do not substitute an unauthorized account or model.
- Run loops in isolated Git worktrees under the same profile-routing prefix.
  When available, use `wt switch -c agent-loop/<task>`.
- Define deterministic verification gates before the loop starts. Tests and
  required checks must pass before its changes are staged or committed.
