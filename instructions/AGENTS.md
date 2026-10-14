# Engineering instructions

Apply these instructions to every developer profile and technology rules
when that technology is involved. Read repository instructions and relevant
documentation before making changes.

## Authority and identity

- Treat repository `AGENTS.md` as canonical; `CLAUDE.md` and `AGY.md` are
  compatibility shims when they delegate to it.
- Use the configured profile, account, Git identity, and permitted tools.
  Obtain identity and routing from configuration, not directory names.
  Never copy credentials between profiles or substitute accounts or clients
  to bypass repository or organizational authorization boundaries.
- Omit automated-assistance attribution from commits, PRs, comments, release
  notes, changelogs, and contributor metadata. Inspect commit and PR text
  before publication; omit attribution signatures and footers.

## Communication and evidence

- Lead with the action or outcome. Use few words and plain language, retaining
  necessary evidence and next steps. Be direct and respectful; avoid filler,
  pleasantries, project-management boilerplate, and curt remarks.
- Carry out settled decisions without editorial commentary. Ask only for
  information or authorization that is actually missing.
- Explain complexity through boundaries, invariants, and refactoring scope,
  not task-duration estimates. Measured runtime remains relevant.
- Missing access, failed tools, and empty output do not establish nonexistence.
  State what could and could not be verified; tool failure is not evidence
  about the requested information.
- If a user-required tool, source, or method is unavailable, fails, returns
  nothing, or requires authentication, stop dependent work. Report `BLOCKED`,
  the attempt, result, and needed user input. Do not substitute sources or
  methods, guess, or infer the answer. Present claims as verified only when
  checked through the required method. Independent authorized work may continue.

## Implementation and verification

- Read files before editing; use available editing tools, preserve unrelated
  changes, and validate inputs early.
- Prefer idiomatic `snake_case`, lowercase acronyms, and intention-revealing
  domain names. Use lowercase log messages and `LOG_LEVEL` for verbosity.
- Keep secrets out of source; use configured secret or environment mechanisms.
  Keep scripts and playbooks idempotent.
- Preserve architectural boundaries. Refactor fragile seams needed for the
  change rather than bypassing them to reduce effort.
- Complete relevant tests, linting, and verification. Report unverified
  behavior; formatting and static checks do not prove runtime behavior.
- When adding developer commands, cover running, testing, supported
  debug/release modes, and applicable memory profiling. Follow the
  `.vscode/tasks.json` schema for editor tasks.
- Comments explain intent, contracts, and rationale. Annotate fixed binary
  sizes with human-readable units, such as `# 200 MiB`.
- Reference source locations with file paths and line numbers.

## No boolean parameters or columns

- Do not introduce boolean function or method parameters, API parameters,
  or database columns, including nullable booleans. This is a prohibition,
  not a preference.
- Express domain meaning through named operations, explicit enums, or domain
  types with meaningful states. Do not disguise booleans as `0`/`1`, strings,
  or flags.
- When changing an existing boolean parameter or column, redesign the affected
  interface or schema. Leave unrelated legacy uses outside the task.
- If compatibility or an external contract prevents a compliant design,
  stop dependent work and report `BLOCKED`: identify the boolean, the
  constraint, and the decision needed from the user. Do not silently retain
  it or introduce an exception.
- Boolean return values, local predicates, and conditional expressions are
  outside this prohibition.

## Git

- Verify configured author and signing identities before committing.
- Use `feat:`, `fix:`, `refactor:`, `chore:`, or `docs:` subjects within
  50 characters; wrap bodies at 72 characters. When the branch contains a
  ticket, prefix subjects with `[TICKET-123]`. Keep conventional text lowercase
  after ticket prefixes in PR titles.
- Omit commit hashes from commit messages and PR titles.
- PR descriptions cover changed behavior, affected modules, verification,
  and manual steps. Add task lists only when requested.
- Before pushing, run `git branch --show-current`, then use plain `git push`.
  Never use refspecs to bypass upstream checks. If an upstream mismatch
  prevents pushing, stop and ask; do not change tracking to bypass it.
- Require explicit authorization to push directly to `main` or `master`.
  Never force-push protected or shared branches.

## AWS

- Before CLI, SDK, or infrastructure operations, check `AWS_PROFILE` and
  `AWS_REGION`. If either is unset, ask for the target before executing.
  Never assume defaults; preserve the configured account boundary.

## SQL and Snowflake

- Execute SQL-capable tool calls sequentially, including across databases.
  Inspect connector capabilities before issuing commands; the database
  product alone does not establish which statements are allowed.
- Inspect an `EXPLAIN` plan before data queries. Use `EXPLAIN ANALYZE` only
  when executing the underlying query is already safe and authorized.
- Check index use or partition pruning. Refine large scans; avoid unbounded
  aggregation, cross joins, and broad filters. Use selective predicates and
  `LIMIT` during exploration; `LIMIT` alone does not bound scan cost.
- Use native syntax for metadata and session commands; do not wrap commands
  that cannot be explained in `EXPLAIN`.
- For each persistent Snowflake session, set `STATEMENT_TIMEOUT_IN_SECONDS`
  to `10` once through an authorized session-control mechanism before data
  queries. Check pruning, including for `SNOWFLAKE.ACCOUNT_USAGE`.
- If required plan inspection or session setup is unavailable, report that
  missing capability and stop dependent queries. Never fabricate successful
  preflight or bypass connector restrictions.
- Require explicit confirmation for `DROP`, `TRUNCATE`, and unfiltered `DELETE`
  or `UPDATE`. Filtered writes still require task authorization.

## Documentation and research

- Read consuming-repository documentation for deployment commands,
  configuration paths, and gateway setup.
- Consult current authoritative documentation for library APIs,
  version-specific behavior, and framework debugging. When Context7 is
  available, resolve the library identifier before querying documentation.
- Use Markdown with terse, coherent headings. Backtick developer literals:
  paths, commands, flags, configuration keys, and resource names.
  Escape Markdown-sensitive generated content.
- When rewriting documentation or comments, remove obsolete narratives about
  prior drafts and implementations that never worked. Preserve the intended
  tense and write as if originally authored this way. Retain only information
  relevant to the described behavior or design.
- Documentation explaining complex architectures or domain models requires
  at least three complementary diagrams: structure, interactions, and
  lifecycle or state behavior. Use consistent domain names and abstractions
  without hiding meaningful complexity.
- Describe discrepancies through the invariant, mismatch, and remedy
  without assigning blame.
- Track stale documentation found during implementation and plan its updates
  separately for user review. Do not silently expand implementation scope;
  approved documentation work may proceed within its agreed scope.

## Autonomous loops

- Before starting, resolve the configured profile and allowed tools.
  Never substitute an unauthorized account or model.
- Use isolated Git worktrees under the same profile-routing prefix.
  Use `wt switch -c agent-loop/<task>` when available.
- Define deterministic verification gates before starting. Tests and required
  checks must pass before staging or committing changes.
