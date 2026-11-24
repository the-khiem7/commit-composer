import re

import pytest
import yaml

from helpers import COMMIT_SKILL_NAMES, ROOT, read_text, rel, split_frontmatter

# This file is the whole test surface of the three skills: the folder shape, the packaged
# copies of the canonical files, and the gate sentence in each SKILL.md.
COMMIT_SKILLS = {
    "commit-composer": "--concise",
    "commit-composer-max": "--max",
}
# The headless skill runs where no shell exists, so it ships the convention only: no kit,
# no scan, no lint. It is classified apart because every gate above needs a shell.
HEADLESS_SKILL = "commit-composer-headless-orca"
ALL_SKILLS = [*COMMIT_SKILLS, HEADLESS_SKILL]

CANONICAL_CONVENTION = ROOT / "contract" / "commit-convention.md"
CANONICAL_KIT = ROOT / "contract" / "commitkit.sh"

# Each skill ships both files because a skill cannot reach a sibling's folder.
SHIPPED = {
    "references/commit-convention.md": CANONICAL_CONVENTION,
    "scripts/commitkit.sh": CANONICAL_KIT,
}

CONVENTION_GATE = (
    "Read `references/commit-convention.md` in full before grouping or writing any "
    "message, every time."
)


def tool_gate(flag):
    return (
        "Run `sh <skill-dir>/scripts/commitkit.sh scan` on the staged diff before every "
        f"commit, and `sh <skill-dir>/scripts/commitkit.sh lint {flag} <msgfile>` on every "
        "message before `git commit -F`."
    )


def skill_text(name):
    return read_text(ROOT / name / "SKILL.md")


def test_every_commit_skill_is_classified():
    assert set(COMMIT_SKILL_NAMES) == set(ALL_SKILLS), (
        f"commit-* folders on disk {sorted(COMMIT_SKILL_NAMES)} differ from ALL_SKILLS "
        f"{sorted(ALL_SKILLS)}: update tests/test_commit_skills.py"
    )


@pytest.mark.parametrize("name", ALL_SKILLS)
def test_skill_frontmatter(name):
    frontmatter, _ = split_frontmatter(skill_text(name))
    assert isinstance(frontmatter, dict), f"{name}/SKILL.md has no frontmatter block"
    assert frontmatter.get("name") == name
    description = frontmatter.get("description")
    assert isinstance(description, str) and description.strip()
    assert len(description) <= 1024, f"{name}: description is {len(description)} characters"
    assert re.fullmatch(r"\d+\.\d+\.\d+", str(frontmatter.get("version"))), (
        f"{name}: version must be a quoted MAJOR.MINOR.PATCH string, written by "
        "scripts/stamp_version.py"
    )


@pytest.mark.parametrize("name", COMMIT_SKILLS)
def test_description_carries_the_words_a_user_would_type(name):
    description = split_frontmatter(skill_text(name))[0]["description"].lower()
    for word in ("commit", "conventional", "hunk"):
        assert word in description, (
            f"{name}: description lacks {word!r}; on a host that is not Codex the "
            "description is the only selection surface"
        )


@pytest.mark.parametrize("name", ALL_SKILLS)
def test_openai_yaml_is_an_explicit_entrypoint(name):
    data = yaml.safe_load(read_text(ROOT / name / "agents" / "openai.yaml"))
    interface, policy = data["interface"], data["policy"]
    for key in ("display_name", "short_description", "default_prompt"):
        assert isinstance(interface.get(key), str) and interface[key].strip()
    assert f"${name}" in interface["default_prompt"]
    assert policy.get("allow_implicit_invocation") is False, (
        f"{name}: a skill that commits is something the user calls, never an agent"
    )
    assert not interface["display_name"].startswith("Baseline Docs"), (
        f"{name}: it is not a baselinedocs skill and must not wear that name"
    )


@pytest.mark.parametrize("name", COMMIT_SKILLS)
def test_folder_shape(name):
    held = {
        path.relative_to(ROOT / name).as_posix()
        for path in (ROOT / name).rglob("*")
        if path.is_file()
    }
    assert held == {"SKILL.md", "agents/openai.yaml", *SHIPPED}, (
        f"{name} holds {sorted(held)}"
    )


@pytest.mark.parametrize("name", COMMIT_SKILLS)
@pytest.mark.parametrize("asset", SHIPPED)
def test_packaged_copy_is_byte_identical(name, asset):
    copy = ROOT / name / asset
    assert copy.read_bytes() == SHIPPED[asset].read_bytes(), (
        f"{rel(copy)} drifted from {rel(SHIPPED[asset])}: edit the canonical file, then copy it"
    )


@pytest.mark.parametrize("name", COMMIT_SKILLS)
def test_skill_requires_the_convention_and_the_checks(name):
    text = skill_text(name)
    assert CONVENTION_GATE in text, f"{name} never requires reading the convention"
    assert tool_gate(COMMIT_SKILLS[name]) in text, (
        f"{name} does not gate commits on scan and on lint {COMMIT_SKILLS[name]}"
    )


@pytest.mark.parametrize("name", COMMIT_SKILLS)
def test_skill_stops_when_the_checks_cannot_run(name):
    assert "do not commit unchecked" in skill_text(name), (
        f"{name}: without sh the secret scan cannot run, and committing unscanned is "
        "the failure the gate exists to prevent"
    )


@pytest.mark.parametrize("name", ALL_SKILLS)
def test_no_dependency_outside_the_skill_folder(name):
    for path in (ROOT / name).rglob("*"):
        if not path.is_file():
            continue
        text = read_text(path)
        assert "../" not in text, f"{rel(path)} reaches outside its folder"
        assert "baselinedocs-" not in text, (
            f"{rel(path)} names a baselinedocs skill: a commit skill installs without the family"
        )


def test_every_skill_carries_the_same_version():
    found = {
        name: split_frontmatter(skill_text(name))[0].get("version") for name in ALL_SKILLS
    }
    assert len(set(found.values())) == 1, f"skills disagree on version: {found}"


def test_each_skill_routes_to_the_other_by_name_only():
    assert "`commit-composer-max`" in skill_text("commit-composer")
    assert "`commit-composer`" in skill_text("commit-composer-max")


def test_no_trailer_rule_survives_in_the_convention():
    text = read_text(CANONICAL_CONVENTION)
    assert re.search(r"No trailer of any kind that names an AI tool or a co-author", text)


def test_headless_folder_shape():
    held = {
        path.relative_to(ROOT / HEADLESS_SKILL).as_posix()
        for path in (ROOT / HEADLESS_SKILL).rglob("*")
        if path.is_file()
    }
    assert held == {"SKILL.md", "agents/openai.yaml", "references/commit-convention.md"}, (
        f"{HEADLESS_SKILL} holds {sorted(held)}: it has no shell, so it ships no kit"
    )


def test_headless_convention_is_byte_identical():
    copy = ROOT / HEADLESS_SKILL / "references" / "commit-convention.md"
    assert copy.read_bytes() == CANONICAL_CONVENTION.read_bytes(), (
        f"{rel(copy)} drifted from {rel(CANONICAL_CONVENTION)}: edit the canonical file, then copy it"
    )


def test_headless_skill_requires_the_convention_and_runs_nothing():
    text = skill_text(HEADLESS_SKILL)
    assert CONVENTION_GATE.replace("grouping or writing any message", "writing the message") in text
    assert "commitkit.sh scan" not in text and "commitkit.sh lint" not in text, (
        "the headless skill cannot run the kit; a sentence telling it to would stall it"
    )
    for word in ("commit", "conventional", "orca"):
        assert word in split_frontmatter(text)[0]["description"].lower()


def test_headless_skill_states_the_output_contract_and_the_orca_version():
    text = skill_text(HEADLESS_SKILL)
    assert "Print the commit message and nothing else." in text, (
        "Orca commits whatever stdout holds, so the skill must forbid a preamble"
    )
    assert re.search(r"Orca \d+\.\d+\.\d+", text), (
        "the skill is written against one Orca version and must say which"
    )


def test_headless_skill_owns_its_prompt_and_needs_only_the_patch():
    text = skill_text(HEADLESS_SKILL)
    assert "{stagedPatch}" in text
    for variable in ("{branch}", "{stagedFiles}", "{linkedIssue}"):
        assert variable not in text.replace("`" + variable + "`", ""), (
            f"{variable} may be named only to say the skill does not use it"
        )
    assert "STOP - no staged patch" in text, (
        "without the patch there is nothing to describe, and the Message box is the only channel"
    )
