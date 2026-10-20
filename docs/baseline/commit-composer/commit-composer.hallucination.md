---
baseline_schema: "2.0"
pack: "commit-composer"
document: "hallucination"
status: "active"
updated: "2026-10-20"
code_ref: "uncommitted"
---

# Commit Composer: Decisions and Open Questions

## Entry index

One row per entry. A row states what the entry is about and nothing more. An answer that turns on an entry whose full text was not read is unbacked.

| Entry | About | Status | Related |
|---|---|---|---|
| CC-D1 | two commit skills committing a working tree at hunk level through a shared convention and a read-only kit | current | CC-D2 |
| CC-D2 | the skills living in their own repository, reversing the rejected separate-repository option of the origin decision | current | CC-D1 |

## CC-D1: `commit-composer` and `commit-composer-max` commit a working tree at hunk level through a shared convention and a read-only kit

Carried over from the `baselinedocs-skills` pack, where it was recorded as FD-D48. It is stated here in full because that repository stops carrying the skills.

**Decided.** Two user entrypoints (`allow_implicit_invocation: false`) in `commit-composer/` and `commit-composer-max/`. Each ships byte-identical copies of `contract/commit-convention.md` (message format, project naming, the rule keeping pack identifiers out of a message, grouping, the whole procedure) and `contract/commitkit.sh` (`hunks`, `patch`, `scan`, `lint`); each `SKILL.md` holds its message shape and two gate sentences. The title is `type(project): subject`; the project is the pack's name, else the nearest manifest. A unit is one `-U0` hunk or a whole unsplittable file, named by a content hash. The skill prints the grouping and commits only after approval. `commit-composer`: title aimed at 50, body optional, 2 to 5 bullets, `lint --concise`. `commit-composer-max`: body always, labelled `Why:`, `Changes:`, `Risk and verification:`, no length limit, `lint --max`. Both print the starting tree id and HEAD id and never push or amend.

**Why.** One file often mixes purposes and `git add -p` is interactive, so an agent needs a non-interactive path to a partial stage. The convention carries the procedure so two `SKILL.md` files do not hold two copies of it. Ids are content hashes because every commit moves line numbers. `patch` recomputes each hunk's new-side start from its old-side start, because `git apply` places a pure insertion by that start and a start taken from the full diff lands it one line early with exit 0 (measured on a scratch repo: after line 20 instead of after 21; a mutation reusing the full-diff start fails 3 tests). The kit only computes, since an installed skill runs in other teams' repositories. A commit outlives the pack and is read by someone who cannot open it, so a pack identifier in a message resolves to nothing.

**What breaks if ignored.** File-level commits mix purposes under one title. A positional unit id names a different hunk after the first commit. A stale offset stages an insertion on the wrong line and reports success. A pack identifier in git history is unresolvable for every later reader. A secret staged without the scan is in history for good.

**Found by running both skills.** Two subagents acted as each skill on a scratch repo with one pack, two projects and one file holding a fix and a feature; each made 4 commits in the right groups, left the tree clean and added no trailer. Their friction changed the convention: a pack that claims no path left the project rule with no answer (now one pack means its name, several or none means the manifest); `scan` and `lint` printed nothing on a pass (now an `OK` line); the tree id alone restored nothing of the commits (now the HEAD id too); a message cited an earlier commit by position (now forbidden, with a `lint` WARN); temp files were left in `.git` (now the operating system's temp folder, deleted at the end); commit types were undefined (now a table).

**Accepted cost.** A unit cannot be split below a `-U0` hunk, so a contiguous region serving two purposes goes with the dominant one. A rename is a deletion plus an addition. `scan` and `lint` read patterns and cannot see a secret without a rule or a wrong reason in a bullet. gawk on Windows strips carriage returns, so the kit passes `BINMODE=3`; a CRLF file's patch failed to apply until a test caught it. The kit ran under gawk only; mawk and BWK awk wait on `.github/workflows/tests.yml`, which has not run. A host with another commit skill that selects itself on staging, such as `caveman-commit` on the author's machine, may compete; both skills are explicit-only and the competition was not observed. Neither skill has been selected by a host from a user request, only run by subagents told to follow it.

**Rejected: scripted `git add -p` with canned input.** Its prompts are interactive and vary by git version.

**Rejected: one skill with a flag for the long message.** Flag handling varies across hosts.

**Rejected: project taken only from a config file.** The user wants the pack name by default and a self scan only when no pack exists.

**Rejected: `[project] type: subject`.** It does not parse as Conventional Commits.

**Rejected: committing without showing the grouping.** Grouping is a judgement and a commit is costly to undo.

**Rejected: a Python or Go kit.** Python is not on every machine an installed skill runs on, and prebuilt binaries are blocked where code integrity policy forbids unsigned executables.

## CC-D2: the skills live in their own repository, with the history of their paths and the release conventions of the family

**Decided.** Split `commit-composer`, `commit-composer-max`, the two canonical files, and the two test files out of `baselinedocs-skills` into this repository with `git filter-repo`, so the history of those paths carries over. The source repository removes the skills entirely. This repository keeps the family's conventions: packaged copies pinned by test, one shared top-level `version:` stamped by `scripts/release.py` and verified by `release.yml`, the three-operating-system `tests.yml`, and a pack under `docs/baseline/`. Initial version `1.0.0`. Pack prefix `CC-`.

**Why.** The skills never read a pack contract, report style or `packtool.sh`, and the family's tests skipped them by folder name, so the coupling was an install and a CI run, not a design. A separate repository gives them their own release number, so a commit-skill fix no longer produces a family release, and a family install no longer carries a skill the user may not want.

**What breaks if ignored.** The repository keeps two unrelated release cadences under one version, and a `--skill` install remains the only way to separate them.

**Accepted cost.** A machine that installed the skills from the old repository keeps those folders: `baselinedocs-self-upgrade` upgrades only `baselinedocs-*` skills and never removes one, so the old copies stay until removed by hand. The user chose to ignore this. The family-map images in the old repository's README were rendered with the two commit chips and are not re-shot by this decision. The `1.0.0` stamp is applied before the first release, so `release.py v1.0.0` finds nothing to commit and only tags. The convention still names baseline packs for project naming and so still describes a concept this repository does not own; it keeps a manifest fallback so it runs without any pack.

**Rejected: keep the skills in the family repository (origin decision, FD-D48).** The user chose that repository at first and accepted the shared install; this entry reverses that choice for the release-cadence reason above.

**Rejected: copy without history.** Loses the history of the convention and the tests, which carry the measured findings in CC-D1.

**Rejected: keep a copy in both repositories.** Two canonical sources for one convention drift, and no test compares across repositories.

**Rejected: version `0.0.0` until the first tag.** The user chose `1.0.0`.

## Open questions

No open question is recorded.
