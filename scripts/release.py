"""Cut a release on this machine: stamp, test, commit, tag. Never pushes.

    uv run scripts/release.py v1.2.3

Stamps the version into every commit-* SKILL.md, runs the suite, commits `release: v1.2.3`
and tags that commit, so the tag holds the stamped tree. It prints the two push
commands and leaves them to you. Stops before any change when the tree is dirty,
the branch is not main, or the tag exists locally or on origin. Local design work is
exempt from the clean-tree check: the `.frontdoor/` folder and a `.gitignore` edit.
Only the stamped SKILL.md files are reverted or committed, so that work is never
lost to a revert or swept into the release commit.
"""
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
import stamp_version  # noqa: E402

# Paths the clean-tree check skips. Neither ships, and a release must not commit them.
LOCAL_ONLY = (".frontdoor/", ".gitignore")


def git(*args, check=True):
    return subprocess.run(
        ["git", *args], cwd=ROOT, capture_output=True, text=True, check=check
    )


def refuse(message):
    print(f"release: {message}", file=sys.stderr)
    return 1


def dirty_paths():
    paths = [line[3:].strip('"') for line in git("status", "--porcelain").stdout.splitlines()]
    return [p for p in paths if not p.startswith(LOCAL_ONLY)]


def stamped():
    return [str(p.relative_to(ROOT).as_posix()) for p in sorted(ROOT.glob("commit-*/SKILL.md"))]


def preflight(tag):
    if git("branch", "--show-current").stdout.strip() != "main":
        return "not on main"
    if dirty_paths():
        return "the working tree has uncommitted changes; commit or stash them first"
    if git("rev-parse", "-q", "--verify", f"refs/tags/{tag}", check=False).returncode == 0:
        return f"tag {tag} already exists locally"
    remote = git("ls-remote", "--tags", "origin", tag, check=False)
    if remote.returncode == 0 and remote.stdout.strip():
        return f"tag {tag} already exists on origin"
    if remote.returncode != 0:
        print("release: could not reach origin; the remote tag check was skipped")
    return None


def main(argv):
    if len(argv) != 2:
        print(__doc__)
        return 2
    try:
        version = stamp_version.parse_version(argv[1])
    except ValueError as error:
        return refuse(str(error))
    tag = f"v{version}"
    problem = preflight(tag)
    if problem:
        return refuse(problem)
    if stamp_version.main(["stamp_version.py", tag]) != 0:
        return refuse("stamping failed")
    uvx = shutil.which("uvx")
    if uvx is None:
        git("checkout", "--", *stamped())
        return refuse("uvx is not on PATH; the stamp was reverted")
    suite = subprocess.run(
        [uvx, "--from", "pytest>=8,<10", "--with", "pyyaml", "pytest", "tests/", "-q"],
        cwd=ROOT,
    )
    if suite.returncode != 0:
        git("checkout", "--", *stamped())
        return refuse("the suite failed; the stamp was reverted and nothing was committed")
    if dirty_paths():
        git("commit", "-m", f"release: {tag}", "--", *stamped())
    git("tag", tag)
    print(f"release: {tag} is committed and tagged. Push it yourself:")
    print("  git push origin main")
    print(f"  git push origin {tag}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
