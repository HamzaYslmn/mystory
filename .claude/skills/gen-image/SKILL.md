---
name: gen-image
description: Generate, create, or make an image, picture, illustration, artwork, cover art or chapter cover on demand using the agy (Antigravity/Gemini) CLI. Also for Turkish requests - görsel üret, resim oluştur, fotoğraf üret, kapak görseli yap. Use whenever an image file has to be produced from a text prompt, and to check the remaining image quota before doing so.
---

# Generate images with agy (Gemini)

`agy` is a Gemini-backed **agent**, not an image API — there is no `agy image` subcommand.
Images come from the agent's `generate_image` tool, wrapped by
`.claude/skills/gen-image/gen-image.ps1`. Paths below are relative to the repo root.

Each image costs a full `agy --print` turn (40-90 s), so speed comes only from running several
at once (`-Parallel`).

## 1. Check quota first

```bash
pwsh -File .claude/skills/gen-image/gen-image.ps1 -Quota
```

```
image model     : gemini-3.1-flash-image
generated total : 13
generated 24h   : 13
last 429 reset  : 2026-07-25 05:33:16 local
status          : BLOCKED, 275 min left
```

A hard server-side cap on the image model, separate from the agent model. **13 images
exhausted it; it reset ~5 h later.** Counts come from agy's output folder, the model and reset
time from the last 429 in `~/.gemini/antigravity-cli/log/`. The *remaining* allowance is not
knowable — no agy command exposes it.

Generation refuses to start while BLOCKED, so a batch can never burn turns against a dead
quota. `-Force` overrides.

## 2. Generate

```bash
pwsh -File .claude/skills/gen-image/gen-image.ps1 -Prompt "a red ceramic teapot on a white table, soft daylight, photorealistic" -Out out/teapot.png
```

For several, use `pwsh -Command` — with `-File` every argument arrives as one literal string,
so `-Prompt 'a','b'` collapses to `a,b` and the pairing silently breaks:

```bash
pwsh -Command "& '.claude/skills/gen-image/gen-image.ps1' -Prompt 'a wet forest road at dusk','a brass lantern in mud' -Out 'a.png','b.png' -Parallel 2"
```

Prints one absolute path per image, warns per failure, exits 1 if any failed.

| Param | Default | Notes |
|---|---|---|
| `-Prompt` | required | One or more. English works clearly better than Turkish. |
| `-Out` | required | Same count as `-Prompt`. `.png` is re-encoded to real PNG, anything else copied as JPEG. Parent dirs created. |
| `-AspectRatio` | 1024x1024 | e.g. `16:9`, `2:3`. Goes to the tool's own `aspect_ratio` argument. |
| `-Ref` | none | Reference image paths, passed as `image_paths`. |
| `-Parallel` | `3` | Concurrent agy processes. |
| `-Model` | `gemini-3.6-flash-high` | The **agent** model. Does not change the image model. |
| `-TimeoutSec` | `420` | Passed to `agy --print-timeout`. |

**Always Read the result before shipping it.** Prompts are followed loosely, no seed, no retry
control.

## Gotchas

- **Left alone the agent regenerates 2-4 times per turn**, retrying after it fails to save the
  file, each retry costing quota. That is how a small batch burns the daily cap in ten minutes.
  The single-call instruction in the driver's prompt is not cosmetic.
- **It reaches for `run_command` to move the file, which kills the run.** Headless mode cannot
  prompt for the `command` permission, so you get `jetski: no output produced` — no result, but
  the image was already generated and the quota already spent. The prompt forbids shell
  commands; do not remove that guard.
- **The tool ignores your output path.** It always writes
  `~/.gemini/antigravity-cli/brain/<conversation-id>/<image_name>_<epoch-ms>.jpg`, always JPEG.
  The driver sets `image_name` to a unique token and matches on it, which is also what makes
  parallel runs safe.
- **Which model draws:** `agy models` lists only agent models. The binary carries
  `gemini-2.5-flash-image-preview` and `gemini-3.1-flash-image-preview`; quota errors name
  `gemini-3.1-flash-image`. Not selectable.
- **Every run re-authenticates**; a cold start can answer with a sign-in message instead of a
  result. The driver retries three times with backoff, and no image is spent.
- `brain/` is never cleaned and doubles as the usage counter for `-Quota`.
- `--dangerously-skip-permissions` works but Claude Code's permission classifier blocks it.

## Troubleshooting

| Symptom | Fix |
|---|---|
| `Image quota ... is exhausted. Resets HH:MM:SS` | Preflight fired, nothing sent. Wait, or `-Force`. Changing `-Model` does not help. |
| `No image produced. agy said: ...` | Read the quoted output. If it mentions the `command` permission, the prompt talked the agent into shelling out — describe only the picture. |
| Prompts paired to the wrong files | You used `pwsh -File` for a multi-image run. Use `-Command`. |
| Half the prompt ignored | Split it: one subject, one setting, one lighting note. |
