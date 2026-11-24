---
baseline_schema: "2.0"
pack: "commit-composer"
document: "hallucination"
status: "active"
updated: "2026-11-24"
code_ref: "8883ed1"
---

# Commit Composer: Decisions and Open Questions

## Entry index

One row per entry. A row states what the entry is about and nothing more. An answer that turns on an entry whose full text was not read is unbacked.

| Entry | About | Status | Related |
|---|---|---|---|
| CC-D1 | two commit skills committing a working tree at hunk level through a shared convention and a read-only kit | current | CC-D2 |
| CC-D2 | the skills living in their own repository, reversing the rejected separate-repository option of the origin decision | current | CC-D1 |
| CC-D3 | an optional tracker-neutral `Refs:` trailer naming the work ticket, taken from the thread, a pack ticket line, or one question | current | CC-D1 |
| CC-D4 | one commit may span the pack documents of one initiative when the action and target are the same | current | CC-D1 |
| CC-D5 | `scan` and `lint` run unpiped, and the commit command is chained behind both so a FAIL stops it | current | CC-D1 |
| CC-D6 | the commit title has no length limit; `--concise` keeps its 50-character WARN | current | CC-D1, CC-D3 |
| CC-D7 | `scan` reports a quoted secret-like assignment inside a test file as a WARN, not a FAIL | current | CC-D1, CC-D5, CC-D6 |
| CC-D8 | a third skill, `commit-composer-headless-orca`, writing one message from the patch Orca's Generate Commit Message dialog sends, with no shell | current | CC-D1, CC-D3, CC-Q1 |
| CC-Q1 | whether the headless skill keeps `agents/openai.yaml` | open | CC-D8 |

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

### CC-Q1: does `commit-composer-headless-orca` keep `agents/openai.yaml`

Orca does not read that file, and a Codex host would never select this skill by its own, since the skill is written for one dialog. `tests/test_commit_skills.py` still pins the file (`test_openai_yaml_is_an_explicit_entrypoint`, `test_headless_folder_shape`) and 2 tests fail while it is absent. The file existed when the suite last passed (41 passed) and was gone at the next run; who removed it is unknown.

Recommendation: restore it with `allow_implicit_invocation: false`, the guard every skill of this repository carries so that no agent selects a skill that commits or stands in for a dialog. Dropping it instead means removing both pins and stating the exception here.

## CC-D3: an optional `Refs: <key> <url>` trailer names the work ticket, from the thread, a pack ticket line, or one question in the plan

**Decided.** The convention allows one `Refs:` line per ticket in the last paragraph, beside any `BREAKING CHANGE:` line; `Refs:` and `BREAKING CHANGE:` are the only trailers. The key is the tracker's own identifier verbatim and the URL is optional. The ticket comes from the user or the thread, else from a pack element's `**Ticket:**` line or task `Ticket:` suffix with inheritance from the nearest enclosing heading, else from one question asked in the plan, with `none` the default. The plan shows each group's `Refs:` line and its source. `lint` accepts `^Refs: ` only as the last paragraph and FAILs `trailer-not-last` otherwise; trailing blank lines do not count as a paragraph break; `ai-trailer` is unchanged. The sentence forbidding AI and co-author trailers stays word for word.

**Why.** A user report (2026-10-29): commits for Redmine work had to end with `Refs: #<id> <url>`, and `lint` failed every such message with `body-not-bullet`, so each commit carried a manual override. The trailer form follows the Conventional Commits footer example, so Jira, GitHub Issues and Redmine keys all fit one rule.

**What breaks if ignored.** Every ticket-referencing commit needs a per-commit lint exception, and an agent that learns to ignore one FAIL stops reading the others.

**Accepted cost.** A ticket URL puts the tracker's host name into history; the convention tells a repository published outside the organization to write the key alone, and nothing checks it. `lint` checks the trailer's place, not that the ticket exists or is the right one.

**Found by running the kit on real messages.** The first version failed the three real commits it was written for: `git log --format=%B` ends with a blank line, which the kit read as a paragraph break after the trailer. Trailing blank lines are now ignored, and a test case carries one.

**Rejected: any `Token: value` trailer.** Lets a stray or attribution-like trailer through, which the AI-trailer rule exists to stop.

**Rejected: a tracker-specific key such as `Redmine:` or `Jira:`.** A second rule per tracker for the same meaning.

**Rejected: the ticket in the title.** Spends title characters the subject needs, and a tracker key is not the effect of the change.

## CC-D4: one commit may span the pack documents of one initiative when the action and target are the same

**Decided.** `contract/commit-convention.md` Grouping gains an initiative exception, copied into both skills: units that are all baseline pack documents, of packs listed under one initiative index, with the same action and the same target, may share one commit whose project is the initiative index pack's name. The plan says so and the user approves it. A unit that is code, or belongs to another initiative, keeps the hard boundary. Owner, 2026-11-10.

**Why.** Repointing links after a diagram folder was removed was one logical change across four packs of one initiative, and the one-project rule split it into four commits (the initiative index, the mesh design, the broker tier and the Workdesk downstream packs) that each said the same thing [user]. The exception keeps the project filter in the log (`git log --grep` on the index pack name finds the cleanup) without a commit per pack [agent].

**What breaks if ignored.** One change is shredded into one commit per pack, and a reader has to assemble it from the log.

**Accepted cost.** The exception rests on the agent reading which packs an initiative index lists and on the user approving the grouping; the kit cannot check either, and no test pins it because the rule is prose. A commit under the index pack name no longer shows which pack each unit sits in; the `Changes:` bullets name each document by role and section.

**Rejected: drop the one-project boundary altogether.** Loses the per-project log filter for code and for units of different initiatives [agent].

**Rejected: allow the exception for any packs in the repository.** Unrelated packs would share a commit and the project name would mean nothing [agent].

## CC-D5: `scan` and `lint` run unpiped, and the commit command is chained behind both so a FAIL stops it

**Decided.** `contract/commit-convention.md` procedure step 4 forbids running `scan` or `lint` through a pipe (`tail`, `head`, `grep`, `tee`), and step 6 gives the commit as `sh commitkit.sh scan && sh commitkit.sh lint <mode flag> <file> && git commit -F <file>`. Copied into both skills. `commitkit.sh` is unchanged. Owner, 2026-11-13.

**Why.** A run printed FAIL from `scan`, the output went through `tail`, and the commit ran anyway [user]. A pipeline returns the status of its last command, so the exit 1 that `scan` gives on FAIL never reached the shell; the rule "never commit while it prints FAIL" then rested on the agent reading the line [agent].

**What breaks if ignored.** A secret or a malformed message is committed although the kit caught it, and a secret in history is there for good.

**Accepted cost.** Nothing enforces the chain: an agent can still run the commit alone. `scan` and `lint` run twice per group (once to read, once in the chain). No test pins the convention text, because it is prose.

**Rejected: make `scan` exit non-zero on FAIL.** It already does (header of `commitkit.sh`, covered by `test_scan_*`); the defect was the pipe hiding the status, not the kit [agent].

**Rejected: leave the stop to the agent reading the FAIL line.** That is the rule that failed [user].

## CC-D6: the commit title has no length limit; `--concise` keeps its 50-character WARN

**Decided.** `lint` no longer FAILs `title-length` at 72 characters in any mode. `contract/commit-convention.md` says the title has no length limit; `commit-composer-max` says "no length limit"; `commit-composer` keeps "aim for 50 characters" and `lint --concise` keeps the WARN `title-length` over 50. `tests/test_commitkit.py` drops the FAIL case and holds `test_lint_sets_no_upper_limit_on_the_title` for `--concise` and `--max`. Owner, 2026-11-13; the 50-character WARN kept by the owner, 2026-11-14.

**Why.** The user asked for the limit to be removed and gave no reason [user]. The 50-character aim is what separates `commit-composer` (short) from `commit-composer-max` (audit-grade), and `assets/skills.webp` shows it, so the user kept it [user].

**What breaks if ignored.** `lint` keeps FAILing titles the user wants to write, and a message that cannot pass is committed by overriding the kit, which teaches the agent to ignore FAIL (see CC-D3).

**Accepted cost.** Views that cut a long title, such as `git log --oneline` in a narrow terminal or a hosting page, show it truncated; nothing now warns for it outside `--concise` [agent].

**Rejected: remove the 50-character aim of `--concise` as well.** Would change both `SKILL.md` files, the README and the rendered image [user].

## CC-D7: `scan` reports a quoted secret-like assignment inside a test file as a WARN, not a FAIL

**Decided.** In `contract/commitkit.sh`, the `credential-assignment` rule prints `WARN credential-assignment-in-test-file <file>:<line>` and does not fail the scan when the file is a test file: a path with a `tests/`, `test/`, `__tests__/` or `spec/` folder, a name `test_*`, a name ending `_test.*`, `.test.*`, `_spec.*` or `.spec.*`, or `*.tftest.hcl` / `*.tftest.json`. The final line then reads `OK scan: no FAIL findings; <n> WARN in test files, read each named line before committing`. A private key block, an AWS access key id and an AWS secret access key assignment stay FAIL in a test file. `contract/commit-convention.md` step 4 tells the agent to check each such line with the value hidden (length, `arn:` prefix, `mock` or `dummy` marker), report it in the run summary and treat a real-looking value as a FAIL. Copied into both skills; `tests/test_commitkit.py` gains cases for six test-file shapes, the two rules that still fail, and a non-test name that must still fail. Owner, 2026-11-18.

**Why.** Terraform and unit-test fixtures mock a secret with a quoted value (a quoted `db_password` value in `*.tftest.hcl`, mock secret ARNs), and a promotion of an existing Terraform tree failed `scan` on 9 such lines, which the owner judged false positives and asked to bypass [user]. A FAIL the agent must override teaches it to read FAIL lines as optional (see CC-D3, CC-D6) [agent]. A WARN keeps the line named in the output, so the check is not silenced [agent].

**What breaks if ignored.** Every commit touching a test fixture needs a manual override of `scan`, and a later real finding is overridden with the same habit.

**Accepted cost.** Pattern matching on a path: a real secret pasted into a file under `tests/` is reported as a WARN and the commit chain `scan && lint && git commit` no longer stops it; only the agent reading the WARN and the key and access-key rules stand in the way. A non-test file that merely resembles a test name (`latest.cfg`) still fails, but a secret placed in a real test folder is not caught as a FAIL [agent]. The rule that stayed FAIL covers key blocks and AWS key ids, not other credential shapes.

**Rejected: bypass every `credential-assignment` FAIL in every file.** Hides a real secret in application config [user chose test files only].

**Rejected: a `--allow-test-files` flag.** The chained commit command would need the flag on every run and an agent can forget it, which reproduces the override habit [agent].

**Rejected: skip test files in `scan` entirely.** A private key block in a fixture is still a leak [agent].

## CC-D8: `commit-composer-headless-orca` writes one message from the patch in the prompt, for Orca's Generate Commit Message dialog, with no shell

**Decided.** A third skill folder `commit-composer-headless-orca` holding `SKILL.md`, a byte-identical copy of `contract/commit-convention.md` in `references/`, and no `scripts/`. It is the Command template of the dialog, not an agent-client entrypoint. The template is `/commit-composer-headless-orca`, a `Mode: max` or `Mode: short` line (missing or unknown means `short`), then `{stagedPatch}`. The skill takes the staged files from the `diff --git` lines of the patch, takes a ticket only from a pack `**Ticket:**` line found with `Grep` (else none, never asked), and does not use `{branch}`, `{stagedFiles}` or `{linkedIssue}`. A checklist in `SKILL.md` stands in for `lint`; a credential in the added lines prints one `chore(secret-check): STOP - ...` line instead of a message. A prompt with no `diff --git` line, or with the diff omitted, prints one `chore(patch-check): STOP - no staged patch ...` line and the skill does not describe the working tree. Output is the message alone. Written against Orca 1.4.272, which `SKILL.md` states. Owner, 2026-11-24.

**Why.** `commit-composer-max` stopped inside the dialog because the session had no Bash and the skill gates every commit on `scan` and `lint` [user]. Orca 1.4.272 (read from the installed bundle, not from its documentation) runs `claude -p --output-format text --model <m> --tools Read,Grep,Glob --allowedTools Read,Grep,Glob --permission-mode dontAsk --strict-mcp-config --settings {"disableAllHooks":true}` with the prompt on stdin; of the user's CLI arguments only `--model` replaces its own, the rest are appended [agent]. It takes all of stdout as the message, cuts a final period from the first line, and falls back to `Update project files` when stdout is empty [agent]. A custom Command template replaces Orca's own prompt, and a variable the template does not name is never sent, so the agent sees no diff unless `{stagedPatch}` is in the template, and it cannot run `git diff --cached` itself [agent]. The user wanted the skill to own the ticket and the file list under the commit composer standard rather than Orca's variables, which could conflict with it [user].

**What breaks if ignored.** A skill that needs a shell halts in the dialog. A template without `{stagedPatch}` gives the agent nothing to describe and invites a message invented from the working tree. Any preamble or code fence the agent prints becomes part of the commit title or body, because stdout is the message.

**Accepted cost.** Never run inside Orca: every Orca fact above comes from reading the bundle, which is minified and changes per version, and nothing yet shows that the dialog resolves `/commit-composer-headless-orca` from the installed skills folder. The size at which Orca cuts the patch is not established. Appending `--allowedTools Bash` through CLI arguments was not tried. The checklist is prose, so only string pins in `tests/test_commit_skills.py` guard it, and `commitkit.sh lint` rules are not run against its output. The copied convention still carries Grouping, Procedure and `commitkit.sh` text that the skill tells the agent to skip, so a reader of that file sees rules this skill does not follow. The `version:` was written by hand to equal the other two (`1.1.0`) so `test_version.py` passes; `scripts/release.py` overwrites it.

**Rejected: a no-shell mode inside `commit-composer-max`.** Grows a `SKILL.md` that holds only what differs, and mixes an interactive procedure with a headless one [user chose the third skill].

**Rejected: the names `commit-composer-ide`, `commit-composer-headless`, `orca-commit-message`.** The first claims coverage of IDEs whose configuration differs, the second names no host, the third leaves the `commit-composer-*` family [user chose `commit-composer-headless-orca`].

**Rejected: a template naming `{branch}`, `{linkedIssue}`, `{stagedFiles}` and `{stagedPatch}`.** Duplicates the ticket and staged-file rules the convention already owns and can disagree with them [user].

**Rejected: granting Bash through the dialog's CLI arguments.** Works against the isolation Orca applies on purpose, and nothing shows that a later `--tools` or `--allowedTools` wins over the one Orca writes [agent].

**Rejected: describing the working tree when the patch is missing.** The message could not be traced to a diff, which defeats the audit purpose of `Mode: max` [user approved the STOP line, 2026-11-24].
