<h1 align="center"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/banner-dark.webp"><img src="assets/banner.webp" alt="commit-composer: messy working tree in, clean single-purpose commits out. A subdivision plat: one parcel is divided into three lots, hatched fix, feat and docs, and recorded as fix(api): expire old tokens, feat(web): add the dark theme and docs(web): explain the theme. A title block reads plan awaits approval, staged nothing yet, approved left blank. Below it: OK scan: no findings in the staged diff, OK lint: no FAIL findings. The two lot lines sway slowly." width="100%"></picture></h1>

**Stop shipping "misc fixes". Point an agent at a messy working tree and get back a clean series of commits, each with one purpose and a title that says it.**

## Install

```bash
npx skills add the-khiem7/commit-composer
npx skills add the-khiem7/commit-composer --skill commit-composer
```

The first line installs both skills, the second only one. Both are explicit entrypoints: call them by name, they never fire on their own. Both need `git` and a POSIX `sh`; without `sh` a skill stops and commits nothing.

<p align="center">
<a href="#how-it-works"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/nav-how-dark.webp"><img src="assets/nav-how.webp" alt="How it works" height="34"></picture></a>
<a href="#two-skills"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/nav-skills-dark.webp"><img src="assets/nav-skills.webp" alt="Two skills" height="34"></picture></a>
<a href="#what-it-will-never-do"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/nav-never-dark.webp"><img src="assets/nav-never.webp" alt="What it will never do" height="34"></picture></a>
<a href="#technical"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/nav-tech-dark.webp"><img src="assets/nav-tech.webp" alt="Technical" height="34"></picture></a>
</p>

## Use it

Call a skill by name in your agent session. These are the prompts each skill ships with:

```text
Use $commit-composer to group my uncommitted changes by project and action at hunk level and commit each group with a short conventional commit message.
```

```text
Use $commit-composer-max to group my uncommitted changes by project and action at hunk level and commit each group with the fullest message, so a later agent can audit the task without reading the code.
```

The agent prints a plan and stops. A plan looks like this; the file, ids and titles here are examples that follow the format in `contract/commit-convention.md`, not output from a real run:

```text
1. fix(api): expire old tokens
   - auth.go -10,0 -> +11,3 (3f9a01c2e4)
   Refs: none, no ticket in the thread
2. feat(api): add token refresh
   - auth.go -40,2 -> +43,2 (8be27d0a51)
   Refs: none, no ticket in the thread
```

You approve, regroup, rename or drop a group. Only then does anything get staged or committed.

## Cut at the hunk, not the file

<picture><source media="(prefers-color-scheme: dark)" srcset="assets/scene-hunks-dark.webp"><img src="assets/scene-hunks.webp" alt="One file. Two purposes. Two commits. A parcel labelled auth.go holds hunk 1, hatched teal, and hunk 2, hatched ochre. It is divided and each half is recorded as its own lot: hunk 1 as fix(api): expire old tokens and hunk 2 as feat(api): add token refresh. Caption: units are named by a hash of the content, so they survive every commit before them." width="100%"></picture>

Real work is tangled: one file holds a bug fix and half a feature. commit-composer splits the working tree into hunks, groups them by project, action, and target, and gives every group its own Conventional Commits message. No `git add -p` sessions, no file-sized compromises.

## How it works

Every run follows the same line, and it always stops at the plan. Nothing is staged or committed until you approve the grouping, and you can regroup, rename, or drop any group first.

<picture><source media="(prefers-color-scheme: dark)" srcset="assets/flow-dark.webp"><img src="assets/flow.webp" alt="The line every change runs on: seven steps from snapshot to report, with a stop at the plan until you approve. The commit runs only if scan and lint both pass." width="100%"></picture>

<details>
<summary>The seven steps as text</summary>

1. Snapshot: keep the tree id and HEAD id.
2. List the hunks with `commitkit.sh hunks`.
3. Name the project and group by project, action and target.
4. Print the plan, naming the ticket, then stop and wait for approval.
5. For each approved group: reset the index, `patch` and `git apply --cached`, then `scan && lint && git commit -F` chained, so the commit runs only if both pass. A FAIL from `scan` or `lint` means no commit. Then the next group.
6. Verify with `git diff HEAD` and `git log --stat`.
7. Report the hashes, the leftover units and both undo ids.

It never pushes, never amends and never uses `--no-verify`.

</details>

Before every commit, two checks run on what is about to land:

| Gate | What it does |
|---|---|
| `commitkit.sh scan` | reads the staged diff for keys and credentials; it names the file and the rule, never the value |
| `commitkit.sh lint` | checks the message against the format; `--concise` or `--max` per skill |

Either one prints FAIL, and that commit does not happen: the two checks run unpiped and chained in front of `git commit`, so a FAIL stops it without anyone reading the output. Both print an `OK` line on a pass.

## Two skills

<picture><source media="(prefers-color-scheme: dark)" srcset="assets/skills-dark.webp"><img src="assets/skills.webp" alt="Pick the lot for the job. commit-composer, short and meaningful: feat(web): add the dark theme with two bullets; title aimed at 50 characters, body optional, 2 to 5 bullets, lint --concise. commit-composer-max, audit-grade, read instead of the diff: the same title with Why:, Changes: as path: symbol - before, now, and Risk and verification: what ran, what was seen; body always, no length limit, lint --max." width="100%"></picture>

| You want | Use | You get |
|---|---|---|
| commits with short, meaningful messages | `commit-composer` | a title aimed at 50 characters and an optional body of 2 to 5 one-line bullets |
| a log another agent can audit without reading the code | `commit-composer-max` | `Why:`, `Changes:`, and `Risk and verification:` blocks naming every changed file and symbol, the risks, and what was checked |

### Inside Orca

`commit-composer-headless-orca` is not for an agent client. It is the Command template of Orca's Generate Commit Message dialog, which runs the agent with `Read`, `Grep`, and `Glob` only: no shell, so no `commitkit.sh`. It writes one message for the staged set from the patch Orca sends, checks it against a checklist in place of `scan` and `lint`, and prints nothing but the message, because Orca commits whatever stdout holds. Written against Orca 1.4.272; other IDEs differ and are not covered.

```text
/commit-composer-headless-orca
Mode: max
{stagedPatch}
```

`Mode: max` gives the audit-grade shape, `Mode: short` the short one. A variable the template leaves out is never sent, and the agent has no shell to read the diff itself, so `{stagedPatch}` is the one Orca variable the skill needs. The staged files come from the patch, and the ticket follows the commit composer rule, not Orca's `{linkedIssue}`. Without a patch the skill prints a one-line STOP in the Message box.

The title is always `type(project): subject`. The project is the name of the baseline pack that claims the changed path, else the folder of the nearest manifest. A message never carries a pack identifier, phase number, or pack filename.

## What it will never do

<picture><source media="(prefers-color-scheme: dark)" srcset="assets/never-dark.webp"><img src="assets/never.webp" alt="Some moves are not on the plat. Five markers stand on the lot line: no push, yours to run; no amend, rebase, tag or branch; no commit before you approve the plan; no commit on FAIL from scan or lint; no AI trailer, no co-author line. Inside the line: approved, scanned, local. Caption: every run ends with a tree id and a HEAD id that undo the index and the new commits." width="100%"></picture>

Every run ends with the starting tree id and HEAD id: `git read-tree <tree id>` restores the index, and `git reset -q <head id>` removes the new commits while keeping every change in the working tree.

## Technical

Both skills ship the same `scripts/commitkit.sh`. It is POSIX sh and POSIX awk only, runs git only to read, and never writes a file, the index, or the network. Every git command that writes is the agent's, so the tool is safe to run inside anyone's repository.

<picture><source media="(prefers-color-scheme: dark)" srcset="assets/tech-units-dark.webp"><img src="assets/tech-units.webp" alt="One diff stream, one awk program, one id: diff_stream feeds UNITS_AWK, which feeds hunks and patch, and patch goes to git apply --cached." width="100%"></picture>

<details>
<summary>The pipeline as text</summary>

- `diff_stream` runs `git diff -U0` against HEAD, or the empty tree when there is no HEAD, then diffs each untracked file against `/dev/null` as a new file, so staged or not, all changes count.
- It feeds `UNITS_AWK`, where a unit is one `-U0` hunk, or a whole file for binary, mode change, submodule or empty files. The id is a hash of the file and the body, with twin units suffixed `.2`, `.3`.
- `UNITS_AWK` feeds two outputs: `hunks`, listing id, file, kind, ranges, counts and a preview; and `patch` with ids, holding only those units with recomputed offsets, which goes to `git apply --cached`.
- The agent runs every git command that writes; `commitkit.sh` only reads and computes.
- It runs on POSIX sh and POSIX awk: dash and mawk, macOS sh and BWK awk, Git for Windows.

</details>

| Command | What it computes |
|---|---|
| `hunks` | one line per unit: id, file, kind, old range, new range, `+added -deleted`, first changed line. Stops when the merge is unresolved |
| `patch <id> ...` | a patch holding only the named units, for `git apply --cached --unidiff-zero`. Exits 1 on an unknown id |
| `scan` | FAIL findings in the staged diff by rule and `file:line`, never the value |
| `lint [--concise\|--max] <msgfile>` | FAIL and WARN findings in a commit message |

Exit status is 0 clean, 1 FAIL present, 2 usage. `scan` and `lint` print an `OK` line on a pass, so a pass never looks like a run that did not happen.

### Ids that survive every commit

A unit id is a hash of its file and content, not its position. Line numbers move after every commit; the content does not, so `hunks` is recomputed before each group and the same ids still name the same changes. `hunks` and `patch` run one shared awk program, so both compute the same id for the same unit.

### Offsets that stay on the right line

<picture><source media="(prefers-color-scheme: dark)" srcset="assets/tech-offset-dark.webp"><img src="assets/tech-offset.webp" alt="Leave a hunk behind, keep the next one on its line: when only hunk 2 of auth.go is in the commit, its new start is the old start plus a shift, and the patch recomputes it." width="100%"></picture>

<details>
<summary>The offset rule as text</summary>

auth.go has two hunks and only hunk 2 is in this commit.

- In the full diff, hunk 1 is `@@ -10,0 +11,3 @@` and hunk 2 is `@@ -40,2 +43,2 @@`. The `+43` counts the 3 new lines of hunk 1.
- In the patch for hunk 2 only, hunk 1 is left out with shift 0, so hunk 2 becomes `@@ -40,2 +40,2 @@`: new start = old start + shift.
- The shift adds new minus old line counts of the selected hunks above. A pure insertion starts at old + 1, a pure deletion at old - 1.
- A start copied from the full diff lands an insertion a line early, and `git apply` still exits 0.

</details>

### What the gates look for

<details>
<summary>The rules of scan and lint, by gate</summary>

| Gate | Rules |
|---|---|
| `scan`, file names | private key files (`.pem`, `.key`, `.p12`, `.pfx`, `.jks`, `.ppk`, `id_rsa` and kin), Terraform state, `.env` files other than examples and templates, an AWS credentials file |
| `scan`, added lines | a private key block, an AWS access key id, an AWS secret access key, a quoted password, secret, token, or API key assignment that is not a placeholder; the assignment is a WARN, not a FAIL, inside a test file (a `tests/` or `spec/` folder, `test_*`, `*_test.*`, `*.test.*`, `*.spec.*`, `*.tftest.hcl`), because a test fixture mocks a secret that way; a key block or an access key id still fails there |
| `lint`, title | `type(project): subject` with one of eleven types, no length limit; WARN over 50 in `--concise` and on a final period |
| `lint`, body | a blank second line, every line a bullet or a label ending in a colon; `--concise` allows no labels and at most 5 bullets, `--max` needs at least one bullet |
| `lint`, anywhere | no en or em dash, no pack identifier, phase number, pack path, or pack filename, no AI or co-author trailer; WARN on a reference to another commit by position and on vague words in `--max` |

</details>

Both gates read patterns. They are a floor, not a verdict: a secret without a rule, or a bullet with an invented reason, passes them.

### Portability

<details>
<summary>Why one file runs under dash, mawk and Git for Windows</summary>

The script sets `LC_ALL=C` and avoids gawk extensions and regex intervals, so one file runs under dash and mawk, macOS sh and BWK awk, and Git for Windows sh and gawk. It passes `BINMODE=3` to awk because gawk on Windows otherwise strips the carriage return from a CRLF file's diff lines, and that patch then fails to apply.

</details>

## Develop

Run the tests with:

```bash
uvx --from "pytest>=8,<10" --with pyyaml pytest tests/ -q
```

Edit the canonical files in `contract/` and copy them into each skill folder; the tests pin the copies byte for byte. The illustrations are drawn in `assets/source/plat.html`, and the commands that render them are in its header comment. A release is `uv run scripts/release.py vMAJOR.MINOR.PATCH`, which stamps the version, runs the tests and tags, and prints the two `git push` commands for you to run.
