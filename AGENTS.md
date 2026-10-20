# Working in this repository

This repo is the source of two skills, `commit-composer` and `commit-composer-max`, split out of the `baselinedocs` skill repository. It follows the same conventions as that family: one canonical asset per concern, byte-identical packaged copies, a shared release version, and tests that pin them.

## What ships and what does not

`npx skills add <repo> --skill <name>` installs a single skill folder. Nothing else travels with it.

| Path | Ships | Read by |
|---|---|---|
| `<skill>/SKILL.md`, `<skill>/agents/openai.yaml`, `<skill>/references/*`, `<skill>/scripts/*` | yes | the running agent |
| `AGENTS.md`, `README.md`, `contract/`, `tests/`, `scripts/`, `.github/`, `docs/baseline/` | no | whoever works in this repo |

- A skill may rely on anything inside its own folder. It never reads a sibling's folder or a path through `../`. Naming the other skill to route a reader to it is fine.
- Do not cut something from a `SKILL.md` because it is written down in `docs/baseline/`. No installed agent can open a doc pack.
- A `SKILL.md` is an instruction executed fresh on every run, not a decision log. Add a WHY clause only where the agent has a plausible reason to break the rule.

## Where reasoning goes

`docs/baseline/commit-composer/` is the decision log: the full argument, the rejected alternatives, and what breaks if a decision is ignored. Identifiers carry the pack prefix `CC-`: `CC-D<n>` decision, `CC-Q<n>` open question, `CC-P<n>` phase. Never write one without its prefix. A commit message never carries one.

## The two canonical assets

Each skill ships byte-identical copies of `contract/commit-convention.md` (message format, project naming, the rule keeping pack identifiers out of a message, grouping, the whole procedure) and `contract/commitkit.sh` (`hunks`, `patch`, `scan`, `lint`). Each `SKILL.md` holds only what differs, the message shape, plus its two gate sentences.

- Edit the canonical file, then copy it into both skills. Never edit a packaged copy.
- `tests/test_commit_skills.py` pins the copies, the folder shape, and the gate sentences.
- `commitkit.sh` is POSIX sh and POSIX awk only: no gawk extension, no regex interval. It computes without writing. Staging and committing are the agent's git commands, never the tool's, because an installed skill runs it inside other teams' repositories. `tests/test_commitkit.py` holds one case per rule and builds its repositories in a temporary directory.
- A unit id is a hash of the file and the hunk body, not a position, because line numbers move after every commit. `patch` recomputes each selected hunk's new-side offset when an earlier hunk of the file is left out.
- Test fixtures that look like a secret are assembled at run time. A scanner reading this repository would otherwise flag the test file.

## Conventions

- ASCII hyphen only. No en dash, no em dash. Enforced by `test_no_typographic_dashes` across every text file Git lists.
- User entrypoints set `allow_implicit_invocation: false`. A skill that commits is something the user calls, never an agent.
- Neither skill names a `baselinedocs-*` skill. Both install without that family.

## Releases

Every `SKILL.md` carries one top-level `version:`, shared by both skills. Never edit it by hand: commit the work to `main`, then run `uv run scripts/release.py vMAJOR.MINOR.PATCH`. It stamps both `SKILL.md` files, runs the suite, commits `release: vX.Y.Z` when the stamp changed anything, and tags that commit, so the tag holds the stamped tree. It never pushes: run the two `git push` commands it prints. `.github/workflows/release.yml` only verifies, with `stamp_version.py --check`, that every `SKILL.md` carries the tag's version.

## Tests

```bash
uvx --from "pytest>=8,<10" --with pyyaml pytest tests/ -q
```

pytest is pinned because bare `uvx pytest` takes whatever is newest. PyYAML is test-only. The repo has no `pyproject.toml`, so `pytest.ini` holds the config. `.gitattributes` forces LF on the byte-compared assets, so the packaged copies compare equal under any `core.autocrlf`.
