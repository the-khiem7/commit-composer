---
baseline_schema: "2.0"
pack: "commit-composer"
document: "roadmap"
status: "active"
updated: "2026-10-20"
code_ref: "uncommitted"
---

# Commit Composer Roadmap

Reasoning for every row lives in `commit-composer.hallucination.md` under the entry named in its Basis column.

## Design area status

| Area | Basis | Status | Evidence |
|---|---|---|---|
| Hunk-level grouping through a shared convention and read-only kit | CC-D1 | implemented, host selection unobserved | `contract/commit-convention.md`, `contract/commitkit.sh`; `tests/test_commit_skills.py` pins copies, folder shape and gates; `tests/test_commitkit.py` holds one case per rule |
| Separate repository | CC-D2 | implemented, first release unobserved | history of the moved paths preserved by `git filter-repo`; `scripts/release.py`, `scripts/stamp_version.py`, `.github/workflows/` carried over |

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

## Next action

Commit the working tree, add a GitHub remote named `commit-composer` under the personal account, then run `uv run scripts/release.py v1.0.0` and the two pushes it prints. Confirm the first `tests.yml` run is green on all three operating systems, since only gawk has run `commitkit.sh`. Then use each skill once on a real working tree and check that a host selects it from a plain request such as "commit these in groups". Nothing in CC-P1 waits on a user decision.
