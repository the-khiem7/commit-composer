---
baseline_schema: "2.0"
pack: "commit-composer"
document: "roadmap"
status: "active"
updated: "2026-10-29"
code_ref: "uncommitted"
---

# Commit Composer Roadmap

Reasoning for every row lives in `commit-composer.hallucination.md` under the entry named in its Basis column.

## Design area status

| Area | Basis | Status | Evidence |
|---|---|---|---|
| Hunk-level grouping through a shared convention and read-only kit | CC-D1 | implemented, host selection unobserved | `contract/commit-convention.md`, `contract/commitkit.sh`; `tests/test_commit_skills.py` pins copies, folder shape and gates; `tests/test_commitkit.py` holds one case per rule |
| Separate repository | CC-D2 | implemented, first release unobserved | history of the moved paths preserved by `git filter-repo`; `scripts/release.py`, `scripts/stamp_version.py`, `.github/workflows/` carried over |
| Work ticket trailer | CC-D3 | implemented, host use unobserved | `contract/commit-convention.md` sections `Message format` and `Work ticket`, procedure step 4; `trailer-not-last` in `contract/commitkit.sh`; seven cases in `tests/test_commitkit.py` |

## CC-P1: split the skills out of `baselinedocs-skills`

Opened and closed 2026-10-20 by the user's decision. CC-D2 carries the reasoning and the rejected options.

Acceptance criteria:

- both skills, both canonical assets and both test files exist here with the history of those paths
- the version is `1.0.0` in both `SKILL.md` files, stamped by `scripts/stamp_version.py`, and the suite checks that they agree
- the suite is green, `test_no_typographic_dashes` included

### Checkpoint: complete, CI and release unobserved

| Item | Result |
|---|---|
| Verification gate | `uvx --from "pytest>=8,<10" --with pyyaml pytest tests/ -q`: 91 passed, 1 skipped (file modes are not tracked on Windows) |
| History | one commit touches the moved paths and it carried over |
| Not observed | `.github/workflows/*.yml` on GitHub; `scripts/release.py` commit and tag path; the first push |
| Commit | uncommitted |

## CC-P2: add the work ticket trailer

Opened and closed 2026-10-29. CC-D3 carries the reasoning and the rejected options.

Acceptance criteria:

- the convention defines an optional tracker-neutral `Refs:` trailer, where the ticket comes from, and how the plan shows it
- `lint` accepts `Refs:` lines only as the last paragraph in both modes, and still FAILs an attribution trailer beside them
- the three real commits that carried the trailer pass `lint --max`
- both skill folders carry byte-identical copies, and the suite stays green

### Checkpoint: complete, host use unobserved

| Item | Result |
|---|---|
| Verification gate | `uvx --from "pytest>=8,<10" --with pyyaml pytest tests/ -q`: 98 passed, 1 skipped (file modes are not tracked on Windows) |
| Field check | `lint --max` printed OK on the three real Redmine-trailer commit messages, after the trailing-blank-line fix |
| Not observed | a host asking for or reading a ticket during a run; mawk and BWK awk on the new branch |

Changes:

| File | Change |
|---|---|
| `contract/commit-convention.md` | `Refs:` in the message format, the only-trailers line, a ticket key read from a pack is not pack content, new section `Work ticket`, procedure step 4 shows the `Refs:` line and its source |
| `contract/commitkit.sh` | `lint`: `refs`, `lastblank`, `last`, `trailer-not-last` |
| `tests/test_commitkit.py` | `REFS`; ticket trailer allowed in both modes and beside `BREAKING CHANGE:`; three `trailer-not-last` cases; `ai-trailer` beside `Refs:` |
| both `SKILL.md` | the pack-reading non-goal names work ticket lines |
| both skill folders | copies of the two canonical files |

## Next action

Commit the working tree, add a GitHub remote named `commit-composer` under the personal account, then run `uv run scripts/release.py v1.0.0` and the two pushes it prints. Confirm the first `tests.yml` run is green on all three operating systems, since only gawk has run `commitkit.sh`. Then use each skill once on a real working tree and check that a host selects it from a plain request such as "commit these in groups". Nothing in CC-P1 waits on a user decision.

After CC-P2, use either skill once on a working tree whose thread names a ticket, and once on one whose pack carries a `**Ticket:**` line, and confirm the plan shows the `Refs:` line with its source. Nothing in CC-P2 waits on a user decision.
