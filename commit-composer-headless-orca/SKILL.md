---
name: commit-composer-headless-orca
description: Write one Conventional Commits message for the staged changes, with no shell and no git, for Orca's Generate Commit Message dialog. It is the Command template of that dialog, not something to call from an agent client. The staged patch arrives in the prompt, the message goes to stdout in a short or an audit-grade shape, and the shell checks of commit-composer are replaced by a checklist. Use only when the prompt carries a Mode line followed by the staged patch from Orca. To group a working tree into several commits from a shell, use commit-composer or commit-composer-max.
version: "1.1.0"
---

# Commit Composer Headless Orca

Written against Orca 1.4.272. Orca starts the agent headless: the Claude CLI runs with `-p`, the tools `Read`, `Grep`, and `Glob` only, no shell, no MCP, no hooks, and the prompt on stdin. Orca takes all of stdout as the commit message, cuts a final period from the first line, and puts the result in its Message box. When Orca changes that, this skill is the part to re-check.

Read `references/commit-convention.md` in full before writing the message, every time. It is the only definition of the message format, how a project is named, what must stay out of a message, and how a ticket is referenced. This skill writes one message for the whole staged set, so skip its Grouping and Procedure sections and every `commitkit.sh` command: nothing here can run them. Do not infer the format from the repository's earlier commits or from memory.

## The prompt

Orca fills the Command template from variables, and a variable the template does not name is never sent. With a custom template Orca sends no diff of its own, and this agent has no shell to run `git diff --cached`, so the staged patch must come through the template. The template this skill expects is these three lines, and nothing else from Orca:

```text
/commit-composer-headless-orca
Mode: max
{stagedPatch}
```

- `Mode: max` writes the audit-grade shape, `Mode: short` the short one. A missing or unknown value means `short`.
- Everything below the Mode line is the staged patch, and it is the only source of what changed. The staged files are the `diff --git a/<path> b/<path>` lines in it. Read a file with `Read` only when the patch leaves a name, a value, or a purpose unclear.
- The skill does not use Orca's `{branch}`, `{stagedFiles}`, or `{linkedIssue}`. The ticket follows the convention's Work ticket rule with what this agent can reach: use a ticket line that `Grep` finds under the baseline folder for the element the change belongs to, else none. Never take a ticket from a branch name or from an issue number, and never ask, because nobody can answer.
- When the text below the Mode line holds no `diff --git` line, or says the diff was omitted, the patch is missing. Do not guess from the working tree: a message that cannot be traced to the diff has no audit value. Print this single line instead of a commit message: `chore(patch-check): STOP - no staged patch in the prompt, add {stagedPatch} to the Command template`.
## Naming the project

Use the order in the convention. With only `Read`, `Grep`, and `Glob`, look for a baseline pack folder by globbing `docs/baseline/**/*.introduction.md`, and read only its frontmatter `pack:` value. A path outside any pack falls to the nearest manifest, the top-level folder, or the repository name. A staged set with two projects takes the one holding most of the changed lines.

## Message shape

`Mode: short`:

- Title: `type(project): subject`, aim for 50 characters.
- Body: leave it out when the title says enough. When the reason is not obvious from the title, add 2 to 5 bullets, each one line, each a single fact, saying why and not what the diff shows. No label lines.

`Mode: max`:

- Title: `type(project): subject`, no length limit.
- Body: always present, in three labelled blocks in this order. Each label line ends with a colon and is followed by one-line bullets. Leave a block out when nothing applies; never write `N/A`.
  - `Why:` the reason and the goal. Nothing in the prompt states a reason, so write `- reason not stated in the staged change` rather than invent one.
  - `Changes:` one bullet per file or symbol, as `path: symbol - what it did before and what it does now`, with exact names, values, paths, and units.
  - `Risk and verification:` what can break and who is affected, and any breaking change. Write `- not verified: nothing was run` because this skill runs nothing.

## Checks in place of scan and lint

Before printing, check the message against each line. The shell versions cannot run here, and a message that breaks one reaches every reader of the log.

- the title matches `type(project): subject` with one of the eleven types, and the line after it is blank
- every body line is a bullet or, in `max`, a label line ending with a colon, one line each, never wrapped
- no en dash or em dash anywhere, only the ASCII hyphen
- no pack identifier, phase number, pack path, pack filename, or the words "doc pack" or "baseline pack"
- no trailer naming an AI tool or a co-author, and no reference to another commit by position
- in `max`, no `various`, `misc`, `some changes`, `and more`, or `etc.`
- `Refs:` and `BREAKING CHANGE:` are the only trailers and they come last

## Secrets

Read the added lines of the patch for a private key block, an AWS access key id, or a quoted password, secret, token, or API key assignment, and for file names such as `.env`, `.pem`, or Terraform state. The message box is the only way to reach the person, so when one is present print this single line instead of a commit message: `chore(secret-check): STOP - staged change holds a possible credential in <file>`. Name the file and never the value.

## Output

Print the commit message and nothing else. No preamble, no quotes, no code fence, no closing remark, because Orca commits whatever stdout holds.

## Non-Goals

- not a commit tool: it writes no file and runs no git, and Orca commits when the user presses Commit
- does not group a working tree into several commits; `commit-composer` and `commit-composer-max` do, from a shell
- not for other IDEs: their prompt, tools, and output handling differ
