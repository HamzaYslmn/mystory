---
name: agy
description: Delegate work to Gemini agents (Flash 3.6 and others) through the agy / Antigravity CLI - run one or many prompts in parallel, keep named multi-turn sessions, feed project files in as context, and generate images. Also for Turkish requests - agenta sor, gemini'ye yaptır, paralel çalıştır, görsel üret, resim oluştur, kapak görseli yap. Use whenever work should be handed to an external Gemini agent instead of being done in this session, and to check image quota before generating.
---

# agy — Gemini agents from the command line

`agy` has no HTTP API, only `agy --print`. One process per task; that is also the only way to
get concurrency. Everything goes through `.claude/skills/agy/agy.py`. Paths are relative to the
repo root.

`agy models` lists what you can pick. Default is `gemini-3.6-flash-high`; `-low` is roughly
3x cheaper and fast enough for extraction and formatting.

## Ask

```bash
python .claude/skills/agy/agy.py ask "Summarize this chapter in five bullets." -f content/stories/kaiser/chapters/01.md
```

Several prompts run **in parallel** (4 processes by default), each in its own conversation:

```bash
python .claude/skills/agy/agy.py ask "Prompt A" "Prompt B" "Prompt C" -j 3
```

`-f` inlines a file ahead of every prompt; repeat it for more. Prints each response, or one
JSON record per prompt with `--json` (`conversation_id`, `status`, `response`,
`duration_seconds`, `num_turns`, `usage`).

| Flag | Default | Notes |
|---|---|---|
| `-f`, `--file` | none | Repeatable. Inlined as `===== FILE: path =====` before the prompt. |
| `-s`, `--session` | none | Named session, see below. |
| `-m`, `--model` | `gemini-3.6-flash-high` | Any name from `agy models`. |
| `-j`, `--jobs` | `4` | Concurrent agy processes. |
| `-t`, `--timeout` | `300` | Seconds, passed to `--print-timeout`. |
| `--json` | off | Raw records instead of just the text. |

## Sessions

`-s NAME` keeps the conversation. The id lives in
`~/.gemini/antigravity-cli/claude-sessions/NAME.id`, one file per name, so different names run
side by side without interfering.

```bash
python .claude/skills/agy/agy.py ask "Read this and remember it." -f docs/economics.md -s econ
python .claude/skills/agy/agy.py ask "Now price a cart axle repair." -s econ
```

Several prompts **with** `-s` run in order, not in parallel: one conversation cannot be driven
from two places at once. Delete the `.id` file to start over.

## Every other agy flag

Anything after `--` is handed to agy verbatim, so the script never has to grow a wrapper per
feature:

```bash
python .claude/skills/agy/agy.py ask "Invent a character." -- --json-schema '{"type":"object","properties":{"name":{"type":"string"},"age":{"type":"integer"}},"required":["name","age"]}'
```

That returns `{"name":"Kaiser Vance","age":28}` — structured output, verified working. Same route
for `--effort`, `--mode plan`, `--mode accept-edits`, `--sandbox`, `--add-dir`, `--agent`,
`--project`, `--new-project`, `--dangerously-skip-permissions`, `--log-file`.

Do **not** pass `--print`, `--output-format` or `--conversation` this way; the script sets those
and a second copy breaks parsing or the session.

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
| `--ref` | none | Reference image path, repeatable. |
| `-j`, `--jobs` | `3` | |
| `-m`, `--model` | `gemini-3.6-flash-high` | The **agent** model. Does not change the image model. |
| `-t`, `--timeout` | `420` | |

Each image costs a full `agy --print` turn (40-90 s), so speed comes only from `-j`. English
prompts work clearly better than Turkish. **Always Read the result before shipping it** — prompts
are followed loosely, no seed, no retry control.

## Gotchas

- **The agent cannot open your files.** Headless mode auto-denies every tool permission
  (`read_file`, `command`, …) because it cannot prompt. That is why `-f` inlines the text
  instead. Fixing it properly means allow-rules under `permissions.allow` in
  `~/.gemini/antigravity-cli/settings.json`.
- **Prompts over ~28k chars do not fit in argv** (Windows caps a command line at 32767). Bigger
  context is split automatically and fed as extra turns of one conversation — correct, but it
  costs a turn per chunk. `power-system.md` alone takes three.
- **Every run re-authenticates**; a cold start can answer with a sign-in message instead of a
  result. The driver retries three times with backoff, and no quota is spent.
- **agy reports failures as a record, not an exit code** — a bad model or a denied tool comes
  back as `status: ERROR` with an `error` field and an empty response. The driver turns that
  into a failure; do not remove the status check or errors will read as blank answers.
- **`--effort` conflicts with a suffixed model.** `-m gemini-3.6-flash-low -- --effort high` is
  rejected. The `-high` / `-medium` / `-low` names already carry the effort; `--effort` is for
  the models listed without one.
- **Left alone the image agent regenerates 2-4 times per turn**, retrying after it fails to save
  the file, each retry costing quota. The single-call instruction in the driver's prompt is not
  cosmetic.
- **It reaches for `run_command` to move the file, which kills the run.** You get
  `jetski: no output produced` — no result, but the image was already generated and the quota
  already spent. The prompt forbids shell commands; do not remove that guard.
- **The image tool ignores your output path.** It always writes
  `~/.gemini/antigravity-cli/brain/<conversation-id>/<image_name>_<epoch-ms>.jpg`, always JPEG.
  The driver tags each request with a unique `image_name` and matches on it, which is also what
  makes parallel runs safe.
- **Which model draws:** `agy models` lists only agent models. Quota errors name
  `gemini-3.1-flash-image`. Not selectable.
- `brain/` is never cleaned and doubles as the usage counter for `quota`.
- `--dangerously-skip-permissions` works but Claude Code's permission classifier blocks it.

## Troubleshooting

| Symptom | Fix |
|---|---|
| `a tool required the "X" permission that headless mode cannot prompt for` | The agent tried to use a tool. Rewrite the prompt so it only needs the text you passed with `-f`. |
| `Image quota ... is exhausted. Resets HH:MM:SS` | Preflight fired, nothing sent. Wait, or `--force`. Changing `-m` does not help. |
| `no image produced. agy said: ...` | Read the quoted output. If it mentions the `command` permission, the prompt talked the agent into shelling out — describe only the picture. |
| Half the prompt ignored | Split it: one subject, one setting, one lighting note. |
| `invalid model selection` | A `--` flag clashes with `-m`. Drop one, usually `--effort`. |
| Something changed in agy | `python .claude/skills/agy/agy.py selftest` — parallel run, session round-trip and chunking, no image quota spent. |
