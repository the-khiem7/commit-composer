# commit-composer

Two skills that turn an uncommitted working tree into a short series of single-purpose commits. Both split changes at hunk level, group them by project, action, and target, show the grouping, and commit only after you approve it. They were split out of the `baselinedocs` skill family and keep its conventions.

| User intent | Skill | Outcome |
|---|---|---|
| Commit with short, meaningful messages | `commit-composer` | Title aimed at 50 characters, an optional body of up to 5 bullets |
| Commit with messages that stand in for reading the code | `commit-composer-max` | A body with the reason, every changed file and symbol, the risks, and what was verified, for task audit |

The title is `type(project): subject`. The project is the name of the baseline pack that claims the changed path, else the nearest manifest. A message never carries a pack identifier, phase number, or pack filename.

Each skill runs a secret scan on the staged diff and a format check on the message before every commit, never pushes and never amends, and prints the ids that undo the index and the commits.

## Install

```bash
npx skills add the-khiem7/commit-composer
npx skills add the-khiem7/commit-composer --skill commit-composer
```

The first line installs both skills, the second one only. Both are explicit entrypoints: invoke them by name, they never fire on their own.

## What each skill folder holds

| Path | Role |
|---|---|
| `SKILL.md` | the message shape and two gate sentences |
| `references/commit-convention.md` | message format, project naming, grouping, the whole procedure |
| `scripts/commitkit.sh` | `hunks`, `patch`, `scan`, `lint`; POSIX sh and awk, read-only |
| `agents/openai.yaml` | explicit-invocation policy and display name |

## Working in this repository

`AGENTS.md` holds the conventions. Run the suite with `uvx --from "pytest>=8,<10" --with pyyaml pytest tests/ -q`. Every `SKILL.md` carries one top-level `version:` shared by both skills; `scripts/release.py` stamps it and tags the stamped commit.
