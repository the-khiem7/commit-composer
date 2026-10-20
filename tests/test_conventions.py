import re

from helpers import read_text, rel, repo_files_matching

# Covers every text file the repo authors, not only markdown. The suffix list is
# the set of text formats present here; an en dash in a skill's openai.yaml or in
# this directory's own Python is as much a convention break as one in a document.
# The set is Git's view of the repo (see helpers.repo_files), so a host skills
# directory installed into this checkout never makes the suite fail on text this
# repo did not author and cannot fix.
TEXT_SUFFIXES = (".md", ".yaml", ".yml", ".txt", ".py", ".ini", ".sh")
# Built from code points so this file does not contain the characters it bans.
TYPOGRAPHIC_DASH = re.compile(f"[{chr(0x2013)}{chr(0x2014)}]")


def test_no_typographic_dashes():
    offenders = []
    for path in repo_files_matching(*TEXT_SUFFIXES):
        for number, line in enumerate(read_text(path).splitlines(), start=1):
            if TYPOGRAPHIC_DASH.search(line):
                offenders.append(f"{rel(path)}:{number}")
    assert offenders == [], (
        f"use the ASCII hyphen, not an en dash or em dash: {', '.join(offenders)}"
    )
