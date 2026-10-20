---
baseline_schema: "2.0"
pack: "commit-composer"
document: "introduction"
status: "active"
updated: "2026-10-20"
code_ref: "uncommitted"
---

# Commit Composer

## Scope

The design of `commit-composer` and `commit-composer-max`: how they group a working tree at hunk level, the shared convention and read-only kit they ship, and why they live in their own repository.

Out of scope, and owned elsewhere:

| Subject | Owner | Why not here |
|---|---|---|
| The baselinedocs family, its pack contract and its release | the `baselinedocs-skills` repository | This pack records only what concerns the two commit skills |
| The rules a running agent obeys | `contract/commit-convention.md` | It ships into both skill folders. This pack records why it says what it says, never what it says |

## Current truth

| Fact | State |
|---|---|
| skills | `commit-composer` (short message, `lint --concise`) and `commit-composer-max` (audit-grade message, `lint --max`). Both `allow_implicit_invocation: false` |
| shared assets | byte-identical copies of `contract/commit-convention.md` and `contract/commitkit.sh` in each skill folder. Pinned by `tests/test_commit_skills.py` |
| kit | `commitkit.sh`: `hunks`, `patch`, `scan`, `lint`. POSIX sh and awk, computes and never writes. Tested by `tests/test_commitkit.py` |
| version | one top-level `version:` in each `SKILL.md`, one value for both, stamped by `scripts/release.py`. Initial value `1.0.0`. CC-D2 |
| origin | split from the `baselinedocs-skills` repository with `git filter-repo`; history of the moved paths preserved. CC-D2 |
| not observed | a host selecting either skill from a plain request; mawk and BWK awk running `commitkit.sh`; `.github/workflows/tests.yml` on three operating systems |
| test command | `uvx --from "pytest>=8,<10" --with pyyaml pytest tests/ -q`, green on Windows with Git for Windows sh and gawk |

## Target

Two explicit-entrypoint skills that commit a working tree in single-purpose groups, never push, and never stage a secret. Reached for the design; the open items are the unobserved rows above.

## Constraints

- A skill may rely only on files inside its own folder. A canonical asset reaches a skill as a byte-identical packaged copy or not at all.
- `README.md`, `AGENTS.md`, `contract/`, `tests/`, `scripts/` and this pack do not ship, so nothing may be cut from a `SKILL.md` on the ground that it is written down here.
- ASCII hyphen only, enforced by `test_no_typographic_dashes`.
- The kit never writes and never touches the network: an installed skill runs it inside other teams' repositories.
- A commit message never carries a pack identifier: the commit outlives the pack and is read by someone who cannot open it.
