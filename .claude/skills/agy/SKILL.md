---
name: agy
description: Delegate work to Gemini agents (Flash 3.6 and others) through the agy / Antigravity CLI - run one or many prompts in parallel, keep named multi-turn sessions, let the agent read project files and edit a file itself, and generate images. Also for Turkish requests - agenta sor, gemini'ye yaptır, paralel çalıştır, dosyayı düzelttir, görsel üret, resim oluştur, kapak görseli yap. Use whenever work should be handed to an external Gemini agent instead of being done in this session, and to check image quota before generating.
---

# agy — Gemini agents from the command line

`agy` has no HTTP API, only `agy --print`. One process per task; that is also the only way to
get concurrency. Everything goes through `.claude/skills/agy/agy.py`. Paths are relative to the
repo root.

`agy models` lists what you can pick. Default is `gemini-3.6-flash-high`; `-low` is roughly
3x cheaper and fast enough for extraction and formatting.

**The agent does the work, this driver decides what lands.** `--add-dir` lets it open project
files itself with `view_file`. Writing into the repo is denied by agy's own rules, but the system
temp directory is granted out of the box, so `edit` stages a copy there, lets the agent edit it
with its own tools, and diffs it back. No settings change, and every result arrives as a
reviewable diff.

## Ask

```bash
python .claude/skills/agy/agy.py ask "Summarize this chapter in five bullets." -f content/stories/kaiser/chapters/chapter4.mdx
```

Several prompts run **in parallel** (4 processes by default), each in its own conversation:

```bash
python .claude/skills/agy/agy.py ask "Prompt A" "Prompt B" "Prompt C" -j 3
```

`-f` does not inline anything; it prepends absolute paths and tells the agent to open them
first. Any size works — a 58k doc is one turn. Prints each response, or one JSON record per
prompt with `--json` (`conversation_id`, `status`, `response`, `duration_seconds`, `num_turns`,
`usage`, and `structured_output` when a schema was used).

| Flag | Default | Notes |
|---|---|---|
| `-f`, `--file` | none | Repeatable. "Read these files first: …" ahead of the prompt. |
| `-s`, `--session` | none | Named session, see below. |
| `-d`, `--dir` | none | Extra readable directory, repeatable. Needed only outside the root. |
| `--root` | cwd | Workspace root handed to `--add-dir`. |
| `-m`, `--model` | `gemini-3.6-flash-high` | Any name from `agy models`. |
| `-j`, `--jobs` | `4` | Concurrent agy processes. |
| `-t`, `--timeout` | `300` | Seconds, passed to `--print-timeout`. |
| `--json` | off | Raw records instead of just the text. |

## Edit a file

```bash
python .claude/skills/agy/agy.py edit content/stories/kaiser/chapters/chapter4.mdx "Apply the brief in the last file." -f .claude/CLAUDE.md -f brief.md
```

The driver copies the target into a fresh temp directory and points the agent at that path. The
agent edits it with `replace_file_content` like it would any file, so a surgical request produces
a surgical diff. Then the driver diffs the working copy against the original, keeps the previous
version as `<name>.bak`, and writes. The repo stays readable but never writable to the agent, and
the working copy is deleted either way.

| Flag | Notes |
|---|---|
| `-f`, `--file` | Extra reading, e.g. the style rules and the task brief. The target is staged automatically. |
| `--dry-run` | Print the diff, write nothing. Same cost, and the next run answers differently, so usually review the real diff instead. |

Keep the prompt one line and put the brief in a `-f` file: a Turkish brief in argv risks console
encoding, and the file is reusable. Tell the brief what must come back untouched (frontmatter,
scene numbers, facts). Read the diff before trusting it; a broad request ("rewrite the chapter")
gets a broad rewrite, and only `.bak` stands between that and the original.

## Sessions

`-s NAME` keeps the conversation. The id lives in
`~/.gemini/antigravity-cli/claude-sessions/NAME.id`, one file per name, so different names run
side by side without interfering.

```bash
python .claude/skills/agy/agy.py ask "Read this and remember it." -f content/stories/kaiser/docs/economics.md -s econ
python .claude/skills/agy/agy.py ask "Now price a cart axle repair." -s econ
```

Several prompts **with** `-s` run in order, not in parallel: one conversation cannot be driven
from two places at once. Delete the `.id` file to start over.

## Permissions

The agent's toolbox is `view_file`, `write_to_file`, `replace_file_content`,
`multi_replace_file_content`, `grep_search`, `list_dir`, `run_command`, `generate_image`,
`search_web`, `read_url_content`, plus subagent and task tools.

Headless mode cannot prompt, so every rule that resolves to `ask` is auto-denied. Ask the agent
to run `list_permissions` to see the live list; the shape that matters:

```
write_file(/): ask                                   every write, unless a later rule wins
command(*): ask                                      no shell
read_file / write_file (agy's own scratch): allowed
read_file / write_file (C:\Users\Asus\AppData\Local\Temp): allowed
read_file / write_file (.env, .git, .netrc, .git-credentials, .npmrc): ask
```

That temp grant is what `edit` runs on, so **nothing has to be configured**. Reading inside an
`--add-dir` directory is likewise free.

To let the agent write straight into the repo you would add one wildcard grant to
`permissions.allow` in `~/.gemini/antigravity-cli/settings.json` — once, not per path — and the
`.env` / `.git` rules above still protect secrets. Claude cannot apply it: editing a permission
file is blocked by Claude Code's classifier, as is `--dangerously-skip-permissions`. Staging
makes it unnecessary anyway.

The related setting `toolPermission` (`always-proceed`, `request-review` (current), `strict`,
`proceed-in-sandbox`) is agy's own auto-approve mode, but it governs **terminal commands only**,
not file writes. `always-proceed` hands the agent an unattended shell; the driver never asks for
one, so leave it alone.

## Every other agy flag

Anything after `--` is handed to agy verbatim, so the script never has to grow a wrapper per
feature:

```bash
python .claude/skills/agy/agy.py ask "Invent a character." -- --json-schema '{"type":"object","properties":{"name":{"type":"string"},"age":{"type":"integer"}},"required":["name","age"]}'
```

That returns `{"name":"Kaiser Vance","age":28}` in `structured_output`. Same route for
`--effort`, `--mode plan`, `--sandbox`, `--agent`, `--project`, `--new-project`, `--log-file`.

Do **not** pass `--print`, `--output-format` or `--conversation` this way; the script sets those
and a second copy breaks parsing or the session. `--add-dir` repeats harmlessly, but use `-d` for
it so the agent's reach stays visible in one place.

Subcommands need no wrapper, run them directly: `agy models`, `agy agents`, `agy plugin list`,
`agy changelog`, `agy update`.

## Images

```bash
python .claude/skills/agy/agy.py quota
python .claude/skills/agy/agy.py image "a brass lantern on wet cobblestones, muted palette" -o out/lantern.png
```

Check quota first. Generation refuses to start while BLOCKED, so a batch can never burn turns
against a dead quota; `--force` overrides. One prompt per output path, same count:

```bash
python .claude/skills/agy/agy.py image "a forest road at dusk" "a broken cart wheel" -o a.png b.png -j 2 --aspect 16:9
```

| Flag | Default | Notes |
|---|---|---|
| `-o`, `--out` | required | One path per prompt. `.png` is re-encoded to real PNG, anything else copied as JPEG. Parent dirs created. |
| `--aspect` | 1024x1024 | e.g. `16:9`, `2:3`. |
| `--ref` | none | Reference image path, repeatable. Resolved to absolute. |
| `-j`, `--jobs` | `3` | |
| `-m`, `--model` | `gemini-3.6-flash-high` | The **agent** model. Does not change the image model. |
| `-t`, `--timeout` | `420` | |

Each image costs a full `agy --print` turn (40-90 s), so speed comes only from `-j`. English
prompts work clearly better than Turkish. **Always Read the result before shipping it** — prompts
are followed loosely, no seed, no retry control.

## Gotchas

- **The agent's cwd is `~/.gemini/antigravity-cli/scratch`, not yours.** A relative path reports
  "file does not exist". The driver states the root and resolves `-f` paths, so pass absolute
  paths in hand-written prompts too.
- **Left alone it reaches for `run_command` to read a file**, which is auto-denied and kills the
  run. The driver's "use view_file, never run_command" line is not cosmetic.
- **A write outside temp is silently fatal, not partial.** The tool is denied, the turn ends with
  an empty response, and nothing on disk changed. Never point the agent at a repo path and hope;
  stage it, which is what `edit` does.
- **Every run re-authenticates**; a cold start can answer with a sign-in message instead of a
  result. The driver retries three times with backoff, and no quota is spent.
- **agy reports failures as a record, not an exit code.** A bad model comes back as a non-SUCCESS
  record with an `error` field. A denied tool is sneakier: `status: SUCCESS`, an empty `response`,
  and the reason only on stderr. The driver fails on an empty answer **that has stderr with it**;
  an empty answer alone is fine, since a turn that only edited a file has nothing to say.
- **`--effort` conflicts with a suffixed model.** `-m gemini-3.6-flash-low -- --effort high` is
  rejected. The `-high` / `-medium` / `-low` names already carry the effort; `--effort` is for
  the models listed without one.
- **A black window still flashes now and then, and the driver cannot stop it.**
  `CREATE_NO_WINDOW` covers the agy process, but agy itself allocates a pseudo-console on some
  runs (caught as a `PseudoConsoleWindow` owned by `agy.exe` and a
  `CASCADIA_HOSTING_WINDOW_CLASS` window appearing in the same second). On Windows 11 the default
  console handler is Windows Terminal, which hosts that in a real window. Setting **Default
  terminal application** to **Windows Console Host** makes the hosting headless and the flash
  goes away; it is a Windows setting, not an agy or driver one.
- **Left alone the image agent regenerates 2-4 times per turn**, retrying after it fails to save
  the file, each retry costing quota. The single-call instruction in the driver's prompt is not
  cosmetic.
- **It reaches for `run_command` to move the image, which kills the run.** You get
  `jetski: no output produced` — no result, but the image was already generated and the quota
  already spent. The prompt forbids shell commands; do not remove that guard.
- **The image tool ignores your output path.** It always writes
  `~/.gemini/antigravity-cli/brain/<conversation-id>/<image_name>_<epoch-ms>.jpg`, always JPEG.
  The driver tags each request with a unique `image_name` and matches on it, which is also what
  makes parallel runs safe.
- **Which model draws:** `agy models` lists only agent models. Quota errors name
  `gemini-3.1-flash-image`. Not selectable.
- `brain/` is never cleaned and doubles as the usage counter for `quota`.

## Troubleshooting

| Symptom | Fix |
|---|---|
| `a tool required the "write_file" permission` | The agent tried to write outside temp. Use `edit`, which stages the file, or add the grant (see Permissions). |
| `a tool required the "read_file" permission` | The path is outside the workspace. Add it with `-d`, or fix `--root`. |
| `edit` prints `no change` | The agent read the working copy and decided nothing was needed, which is often correct. Check the premise before rewording the prompt. |
| The diff is far bigger than asked | The agent rewrote rather than patched. Restore from `.bak` and name the passage to touch. |
| `Image quota ... is exhausted. Resets HH:MM:SS` | Preflight fired, nothing sent. Wait, or `--force`. Changing `-m` does not help. |
| `no image produced. agy said: ...` | Read the quoted output. If it mentions the `command` permission, the prompt talked the agent into shelling out — describe only the picture. |
| Half the prompt ignored | Split it: one subject, one setting, one lighting note. |
| `invalid model selection` | A `--` flag clashes with `-m`. Drop one, usually `--effort`. |
| Something changed in agy | `python .claude/skills/agy/agy.py selftest` — parallel run in separate conversations, session round-trip, `--dry-run` writing nothing, and a real edit; no image quota spent. |
