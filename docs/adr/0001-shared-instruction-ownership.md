# 1. Centralize shared engineering instructions

## Status

Accepted.

## Context

Dotfiles distributes the same instruction document to every developer profile,
but retains additional client copies. Those copies drift independently from
the canonical document. Account routing and machine setup are already owned
by the profile configuration; embedding their values in shared instructions
creates another configuration source.

## Decision

This repository owns shared engineering and technology policies through the
self-contained `instructions/AGENTS.md` interface. Dotfiles owns installation,
identity routing, credentials, and permissions, consuming a Git revision pinned
in its Nix lock file. All profiles receive identical instructions.

A single document keeps loading independent of client include syntax. Topic
files and generated bundles would add an assembly contract without changing
the required output. Branch-fetching activation could update independently of
dotfiles, but would make activation network-dependent and weaken rollback.

The validator and model review are adapted from `awill1988/agent-skills` at
revision `6b955db2c85b683e7ad04b6262cff35b140d1338`. Prompt validation does not
apply skill metadata or marketplace rules. The tools are maintained here;
installation does not depend on another tooling repository.

## Invariants and abstention

- Keep the distribution path stable and its content self-contained.
- Respect configured authorization boundaries without reproducing identities.
- Do not fall back to embedded dotfiles policy when fetching fails.
- Missing or incomplete model execution cannot produce approval.
- Require both CI checks before merging instruction changes.
- Do not activate a consumer revision before validating its installed outputs.

## Consequences

Instruction revisions have independent review history and deterministic checks.
Nix deployments retain reproducibility and generation rollback. Prompt updates
require a consumer lock update; publishing alone does not change installed
instructions. Model assessment supplements human review and tests; it does not
establish behavioral correctness.

The review model uses the existing collection's baseline. The runner archive
is additionally checksum-pinned and re-extracted from verified bytes. Results
are job summaries and artifacts, not formal approvals or posted comments.
