# Policy migration

Every profile receives one document. Identities, permissions, and machine setup
remain properties of the consuming environment.

| Previous section | Treatment | Result |
| --- | --- | --- |
| Highest Priority Policy; No AI Attribution | Consolidated | One authority and attribution policy; publication text still requires inspection. |
| Profile | Consolidated | Direct, respectful communication and settled-decision handling. |
| Standards; Standard Variables | Retained | Idiomatic naming, lowercase logs, and `LOG_LEVEL`. |
| Practices; Tool Preferences | Revised | Read-before-edit and input validation remain; editing uses available tools. Debug/release and profiling apply where supported. |
| Git Workflow; Push Safety | Retained | Identity checks, subject/body limits, tickets, protected branches, plain push, and refusal handling. Git settings are no longer asserted universally. |
| AWS Operations | Generalized | Explicit profile and region remain; machine-specific examples are removed. |
| SQL Operations | Clarified | Sequential queries and data-query plan inspection remain. Metadata and session commands use native syntax. `LIMIT` does not establish bounded scan cost. |
| Snowflake MCP | Revised | Timeout and pruning checks remain. Discovered capabilities replace an allowlist that contradicted required commands. Unsupported preflight blocks dependent queries. |
| Context7 MCP | Generalized | Authoritative documentation remains required; use the resolve/query workflow when available. |
| MCP Sync | Relocated | Consuming documentation owns gateway configuration and deployment commands. |
| Documentation Authoring; Documentation Maintenance | Retained | Literal formatting, escaping, blameless corrections, and separate user-reviewed documentation work. |
| Engineering Rigor | Consolidated | Architectural boundaries, required refactoring, and verification; no task-duration estimates. |
| AI Assistant Ecosystem | Removed | Product and provider descriptions are unnecessary policy and become stale. |
| Developer Profiles and Identity Routing | Generalized | Configured boundaries remain mandatory; account names, emails, and directory mappings are not duplicated. |
| Continuous Agent Loops | Generalized | Configured authorization, isolated worktrees, and deterministic verification remain. |
| Initial README reference | Removed | Installed policy has no repository-relative README dependency. |

SQL capability handling, tool portability, and conditional developer flows are
substantive clarifications. Removing identities does not expand authorized
accounts or clients: configured boundaries govern every operation.

## Saved instruction integration

### Policy changes

- Evidence and blockers: missing access, failed tools, and empty output cannot
  establish nonexistence. Failure or empty output from a user-required tool,
  source, or method stops dependent work with a `BLOCKED` report stating the
  attempt, result, and needed user input. Substitutes and inferred answers are
  prohibited; independent authorized work may continue.
- Documentation and comments: remove obsolete draft and failed-implementation
  storytelling, preserve the intended tense, and retain only relevant content.
  No completed-PR or historical-decision exceptions are added.
- Complex models: require at least three complementary diagrams covering
  structure, interactions, and lifecycle or state behavior. This generalizes
  the PRG-specific request to complex architecture and domain documentation.

### Editorial consolidation

- Communication: consolidate the saved preference into the existing concise,
  respectful style rule, emphasizing few words and plain language while
  retaining necessary evidence and action. Omit generational labels and
  personal circumstances from shared policy.
- Integrate the saved notes into the self-contained distribution document;
  normalize wording without retaining standalone prompt titles or emphasis.

## Concise policy and boolean interfaces

### Policy addition

- Prohibit new boolean function, method, and API parameters and database
  columns, including nullable booleans and disguised boolean flags. Use named
  operations, explicit enums, or domain types with meaningful states instead.
- Changing an existing boolean parameter or column requires redesign of the
  affected interface or schema. Unrelated legacy uses remain outside scope.
  Compatibility or external-contract constraints block dependent work until
  the user supplies the needed decision; they do not permit silent exceptions.
- Boolean return values, local predicates, and conditional expressions remain
  outside the prohibition. This policy update does not migrate application
  schemas or refactor other repositories.

### Editorial consolidation

- Combine communication and evidence, consolidate identity and Git wording,
  and shorten implementation, database, documentation, and loop instructions.
  Preserve existing requirements, exceptions, and stopping conditions.
- Keep the distribution self-contained. No installation or tooling changes
  accompany the rewrite.
