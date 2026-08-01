#!/usr/bin/env python3
"""Drive the agy (Antigravity/Gemini) CLI from Claude Code.

agy has no HTTP API, only `agy --print`; one process per task is also the only way to get
concurrency. The agent reads project files itself, since `view_file` needs no permission inside
an `--add-dir` workspace. Writing anywhere else is `ask`, which headless mode auto-denies, but
agy ships a standing grant for the system temp directory. So `edit` stages a copy there, lets
the agent edit it with its own tools, then diffs it back: no settings change, and the write into
the repo stays on this side. Anything after `--` is handed to agy verbatim.
"""
from __future__ import annotations

import argparse
import difflib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
import uuid
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

AGY = shutil.which("agy") or "agy"
HOME = Path.home() / ".gemini" / "antigravity-cli"
BRAIN, LOGS = HOME / "brain", HOME / "log"
SESSIONS = HOME / "claude-sessions"   # one file per name: concurrent sessions never collide
MODEL = "gemini-3.6-flash-high"
AUTH_RE = re.compile(r"not logged in|signing in|sign in to|log in to|"
                     r"authenticat\w* fail|no token|token source", re.I)
# agy is a .cmd shim on Windows, so every turn would flash a console window without this.
NO_WINDOW = {"creationflags": 0x08000000} if os.name == "nt" else {}   # CREATE_NO_WINDOW

# The agent's own cwd is agy's scratch folder, so relative paths silently miss. Left to itself it
# also reaches for run_command to read a file, which headless mode auto-denies and the run dies.
PREAMBLE = ("You are working inside {root}\n"
            "Open files with the view_file tool and absolute paths. Never use run_command.\n\n")

EDIT_RULES = (
    "Edit {stage} in place with replace_file_content.\n"
    "It is a working copy: edit that exact path, create no other file, write no summary of what "
    "you did anywhere.\n"
    "Make the smallest change that does the job and leave every other byte alone, frontmatter "
    "included.\n\nTask: ")


class AgyError(RuntimeError):
    pass


def run(prompt: str, a, conv: str | None = None) -> dict:
    """One `agy --print` turn. Returns the parsed JSON record."""
    cmd = [AGY, "--print", PREAMBLE.format(root=a.root) + prompt, "--model", a.model,
           "--output-format", "json", "--print-timeout", f"{a.timeout}s"]
    for d in [a.root, *a.dir]:
        cmd += ["--add-dir", d]
    if conv:
        cmd += ["--conversation", conv]
    cmd += a.extra

    # Every run re-authenticates; a cold start can answer with a sign-in message instead of a
    # result. Nothing is spent then, so retry. Any other non-JSON output is a real failure
    # (usually a tool permission auto-denied in headless mode) and must not be retried.
    for attempt in (1, 2, 3):
        try:
            p = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8",
                               errors="replace", timeout=a.timeout + 30, **NO_WINDOW)
        except subprocess.TimeoutExpired:
            raise AgyError(f"no answer within {a.timeout + 30}s")
        for line in reversed(p.stdout.splitlines()):
            if line.startswith("{"):
                rec = json.loads(line)
                # agy reports a bad model or a timeout as a record, not an exit code, so the
                # status has to be checked or failures pass as empty answers.
                status = rec.get("status", "no status in the record")
                if status != "SUCCESS":
                    raise AgyError(rec.get("error") or rec.get("response") or status)
                # A denied tool is worse: SUCCESS, an empty response, and the reason only on
                # stderr. An empty response on its own is not a failure, though; a turn that
                # only edited a file has nothing to say.
                if not rec.get("response", "").strip() and p.stderr.strip():
                    raise AgyError(p.stderr.strip())
                return rec
        out = (p.stdout + p.stderr).strip()
        if not AUTH_RE.search(out):
            raise AgyError(out or f"agy exited {p.returncode} with no output")
        time.sleep(3 * attempt)
    raise AgyError(out)


def turn(prompt: str, a) -> dict:
    """One prompt, resuming and saving `a.session` if there is one."""
    if a.file:
        prompt = ("Read these files first: "
                  + ", ".join(str(Path(f).resolve()) for f in a.file) + "\n\n" + prompt)
    f = a.session and session_file(a.session)
    conv = f.read_text(encoding="utf-8").strip() if f and f.exists() else None
    rec = run(prompt, a, conv)
    if f and rec.get("conversation_id"):
        f.write_text(rec["conversation_id"], encoding="utf-8")
    return rec


def session_file(name: str) -> Path:
    SESSIONS.mkdir(parents=True, exist_ok=True)
    return SESSIONS / (re.sub(r"[^A-Za-z0-9_.-]", "_", name) + ".id")


def pmap(fn, items, jobs):
    """Map, keeping exceptions as values so one bad task cannot kill the batch."""
    def guarded(it):
        try:
            return fn(it)
        except Exception as e:
            return e
    with ThreadPoolExecutor(max_workers=max(1, jobs)) as ex:
        return list(ex.map(guarded, items))


def emit(labels, values, header=False) -> int:
    for label, v in zip(labels, values):
        if isinstance(v, Exception):
            print(f"FAILED {label}: {v}", file=sys.stderr)
            continue
        if header:
            print(f"===== {label} =====")
        print(v)
    return 1 if any(isinstance(v, Exception) for v in values) else 0


def cmd_ask(a) -> int:
    # A session is one conversation and cannot be driven from two places at once, so -s runs
    # its prompts in order.
    recs = pmap(lambda p: turn(p, a), a.prompt, 1 if a.session else a.jobs)
    out = [r if isinstance(r, Exception)
           else json.dumps(r, ensure_ascii=False) if a.json
           else r["response"].rstrip() for r in recs]
    return emit([f"[{i}]" for i in range(1, len(recs) + 1)], out,
                header=len(recs) > 1 and not a.json)


def cmd_edit(a) -> int:
    """The agent edits a working copy with its own tools; this decides what reaches the repo."""
    target = Path(a.target).resolve()
    before = target.read_text(encoding="utf-8")
    # tempfile's root is the one directory agy grants write access to out of the box, so no
    # settings change is needed. Check `list_permissions` if a write is ever denied here.
    with tempfile.TemporaryDirectory(prefix="agy-", ignore_cleanup_errors=True) as tmp:
        stage = Path(tmp) / target.name
        stage.write_text(before, encoding="utf-8")
        turn(EDIT_RULES.format(stage=stage) + a.prompt, a)
        after = stage.read_text(encoding="utf-8")
    if not after.strip():
        raise AgyError("the working copy came back empty, file untouched")

    diff = list(difflib.unified_diff(before.splitlines(True), after.splitlines(True),
                                     f"{target.name} before", f"{target.name} after"))
    if not diff:
        print("no change")
        return 0
    sys.stdout.writelines(diff)
    if a.dry_run:
        print("\n--dry-run: nothing written")
        return 0
    bak = target.with_suffix(target.suffix + ".bak")
    bak.write_text(before, encoding="utf-8")
    target.write_text(after, encoding="utf-8")
    plus = sum(1 for l in diff if l.startswith("+") and not l.startswith("+++"))
    minus = sum(1 for l in diff if l.startswith("-") and not l.startswith("---"))
    print(f"\nwrote {target} (+{plus} -{minus} lines), previous version kept at {bak.name}")
    return 0


def quota():
    """Image model, reset time and blocked flag, read from the last 429 agy logged. The
    remaining allowance is server-side and no agy command exposes it."""
    for log in sorted(LOGS.glob("cli-*.log"), key=lambda p: p.stat().st_mtime, reverse=True):
        blob = log.read_text(encoding="utf-8", errors="replace")
        stamps = re.findall(r'"quotaResetTimeStamp":\s*"([^"]+)"', blob)
        if stamps:
            reset = datetime.fromisoformat(stamps[-1].replace("Z", "+00:00"))
            models = re.findall(r'"model":\s*"([^"]+)"', blob)
            return (models[-1] if models else None), reset, reset > datetime.now(timezone.utc)
    return None, None, False


def brain_images():
    return [p for p in BRAIN.rglob("*") if p.suffix.lower() in (".jpg", ".jpeg", ".png")
            and ".tempmediaStorage" not in str(p)]


def gen_image(prompt: str, out: str, a) -> Path:
    """The tool always writes JPEG into agy's own conversation folder and ignores the requested
    path, so each request carries a unique image_name and is matched on it. That tag is also
    what makes parallel runs safe."""
    token = "gi" + uuid.uuid4().hex[:10]
    guard = ["Do NOT use run_command or any shell command. Do NOT try to move, copy or rename "
             "the file.",
             "Use ONLY the generate_image tool, exactly once, then stop.",
             f"Pass image_name exactly: {token}"]
    if a.aspect:
        guard.append(f"Pass aspect_ratio exactly: {a.aspect}")
    if a.ref:
        guard.append("Pass image_paths: " + ", ".join(str(Path(r).resolve()) for r in a.ref))
    guard += ["", f"Generate this image: {prompt}"]

    since, err = time.time() - 60, ""
    try:
        run("\n".join(guard), a)
    except AgyError as e:
        err = str(e)   # the image can exist even when the turn ended badly, so look anyway
    hits = [p for p in brain_images()
            if p.name.startswith(token) and p.stat().st_mtime > since]
    if not hits:
        raise AgyError(f"no image produced. agy said: {err or '(nothing)'}")

    dst = Path(out)
    dst.parent.mkdir(parents=True, exist_ok=True)
    src = max(hits, key=lambda p: p.stat().st_mtime)
    if dst.suffix.lower() == ".png":
        from PIL import Image
        with Image.open(src) as im:
            im.convert("RGB").save(dst, "PNG")
    else:
        shutil.copyfile(src, dst)
    return dst.resolve()


def cmd_image(a) -> int:
    if len(a.prompt) != len(a.out):
        sys.exit(f"{len(a.prompt)} prompts but {len(a.out)} outputs.")
    model, reset, blocked = quota()
    if blocked and not a.force:
        left = int((reset - datetime.now(timezone.utc)).total_seconds() // 60)
        sys.exit(f"Image quota for {model} is exhausted. Resets {reset.astimezone():%H:%M:%S} "
                 f"local ({left} min). Nothing was sent. Re-run then, or pass --force.")
    paths = pmap(lambda io: gen_image(io[0], io[1], a), list(zip(a.prompt, a.out)), a.jobs)
    return emit(a.out, paths)


def cmd_quota(a) -> int:
    model, reset, blocked = quota()
    imgs = brain_images()
    print(f"image model     : {model or 'gemini-3.1-flash-image (assumed; no 429 yet)'}")
    print(f"generated total : {len(imgs)}")
    print(f"generated 24h   : {sum(p.stat().st_mtime > time.time() - 86400 for p in imgs)}")
    if reset:
        left = int((reset - datetime.now(timezone.utc)).total_seconds() // 60)
        print(f"last 429 reset  : {reset.astimezone():%Y-%m-%d %H:%M:%S} local")
        print(f"status          : BLOCKED, {left} min left" if blocked
              else "status          : OK, quota window has reset")
    else:
        print("status          : OK, no quota error recorded")
    print("note            : remaining allowance is server-side; agy cannot query it.")
    return 0


def cmd_selftest(_) -> int:
    t0 = time.time()
    a = argparse.Namespace(model="gemini-3.6-flash-low", timeout=150, extra=[], file=[],
                           dir=[], root=os.getcwd(), session=None)

    recs = pmap(lambda p: turn(p, a), ["Reply with exactly: ALPHA", "Reply with exactly: BETA"], 2)
    assert not any(isinstance(r, Exception) for r in recs), recs
    assert {r["response"].strip() for r in recs} == {"ALPHA", "BETA"}, recs
    assert recs[0]["conversation_id"] != recs[1]["conversation_id"], "parallel runs shared a conversation"

    a.session = "selftest-" + uuid.uuid4().hex[:6]
    turn("Remember the number 4711. Reply OK.", a)
    back = turn("What number did I ask you to remember? Digits only.", a)
    assert "4711" in back["response"], back["response"]
    session_file(a.session).unlink(missing_ok=True)
    a.session = None

    # The agent opens and edits the working copy itself; --dry-run must still leave the real
    # file alone, and everything it was not asked to touch must survive byte for byte.
    start = "alpha\nMARKER=ZQ7\nomega\n"
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp:
        d = Path(tmp)
        a.root = tmp
        (d / "t.txt").write_text(start, encoding="utf-8")
        ns = argparse.Namespace(**vars(a), target=str(d / "t.txt"), dry_run=True,
                                prompt="Change ZQ7 to QP9.")
        assert cmd_edit(ns) == 0
        assert (d / "t.txt").read_text() == start, "--dry-run wrote"
        ns.dry_run = False
        assert cmd_edit(ns) == 0
        assert (d / "t.txt").read_text() == start.replace("ZQ7", "QP9"), "edit went wrong"

    print(f"selftest OK ({time.time() - t0:.1f}s)")
    return 0


def main() -> int:
    argv, extra = sys.argv[1:], []
    if "--" in argv:                      # everything after `--` is handed to agy verbatim
        i = argv.index("--")
        argv, extra = argv[:i], argv[i + 1:]

    ap = argparse.ArgumentParser(
        description=__doc__.split("\n\n")[0],
        epilog="Flags after `--` go straight to agy, e.g. `-- --effort high --sandbox`. "
               "Do not override --print, --output-format or --conversation; for --add-dir use -d.")
    sub = ap.add_subparsers(dest="cmd", required=True)

    def common(p, jobs=1, timeout=300):
        p.add_argument("-m", "--model", default=MODEL)
        p.add_argument("-j", "--jobs", type=int, default=jobs, help="concurrent agy processes")
        p.add_argument("-t", "--timeout", type=int, default=timeout, help="seconds")
        p.add_argument("-d", "--dir", action="append", default=[],
                       help="extra directory the agent may read (repeatable)")
        p.add_argument("--root", default=os.getcwd(), help="workspace root the agent may read")
        p.set_defaults(session=None, file=[])
        return p

    k = common(sub.add_parser("ask", help="run prompts, in parallel by default"), 4)
    k.add_argument("prompt", nargs="+")
    k.add_argument("-s", "--session", help="named session; resumes the same conversation")
    k.add_argument("--json", action="store_true", help="raw JSON record instead of the text")
    k.set_defaults(fn=cmd_ask)

    e = common(sub.add_parser("edit", help="agent edits a temp copy; driver diffs it in"),
               timeout=420)
    e.add_argument("target", help="the file to change")
    e.add_argument("prompt", help="what to change (long briefs belong in a -f file)")
    e.add_argument("--dry-run", action="store_true", help="print the diff, write nothing")
    e.set_defaults(fn=cmd_edit)

    # -f only reaches the agent through turn(); gen_image calls run() directly, so image has none.
    for p in (k, e):
        p.add_argument("-f", "--file", action="append", default=[],
                       help="file the agent is told to read first (repeatable)")

    g = common(sub.add_parser("image", help="generate images"), 3, 420)
    g.add_argument("prompt", nargs="+")
    g.add_argument("-o", "--out", nargs="+", required=True, help="one path per prompt")
    g.add_argument("--aspect", help="e.g. 16:9, 2:3")
    g.add_argument("--ref", action="append", default=[], help="reference image (repeatable)")
    g.add_argument("--force", action="store_true", help="ignore the quota preflight")
    g.set_defaults(fn=cmd_image)

    sub.add_parser("quota", help="image quota status").set_defaults(fn=cmd_quota)
    sub.add_parser("selftest", help="round-trip check; spends no image quota").set_defaults(
        fn=cmd_selftest)

    a = ap.parse_args(argv)
    a.extra = extra
    try:
        return a.fn(a)
    except (AgyError, OSError) as e:
        sys.exit(str(e))


if __name__ == "__main__":
    sys.exit(main())
