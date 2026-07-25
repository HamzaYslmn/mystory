<#
.SYNOPSIS
  Generate images on demand with the agy (Antigravity/Gemini) CLI.

.DESCRIPTION
  agy has no image API, only an agent with a `generate_image` tool. That tool always writes
  into its own conversation folder under ~/.gemini/antigravity-cli/brain/ and always as JPEG,
  ignoring the output path you ask for. This script drives one agy process per image, tags each
  request with a unique image name so concurrent runs can tell their own output apart, and
  copies the result where you asked.

  Image quota is per image model and server-side. Before spending anything it reads the last
  429 out of agy's own logs; if the reset time has not passed yet it refuses to run.

.EXAMPLE
  .\gen-image.ps1 -Quota

.EXAMPLE
  .\gen-image.ps1 -Prompt "a red ceramic teapot" -Out out/teapot.png

.EXAMPLE
  .\gen-image.ps1 -Prompt "a forest road","a lantern in mud" -Out a.png,b.png -AspectRatio 16:9
#>
[CmdletBinding()]
param(
  [string[]]$Prompt,
  [string[]]$Out,
  [string]$AspectRatio,
  [string[]]$Ref,
  [string]$Model = 'gemini-3.6-flash-high',
  [int]$Parallel = 3,
  [int]$TimeoutSec = 420,
  [switch]$Quota,
  [switch]$Force
)

$ErrorActionPreference = 'Stop'
$agyHome = Join-Path $env:USERPROFILE '.gemini\antigravity-cli'
$brain = Join-Path $agyHome 'brain'
$logDir = Join-Path $agyHome 'log'

function Get-QuotaStatus {
  # The 429 body agy logs carries the model and an exact reset timestamp. That is the only
  # real quota signal available locally; the remaining allowance is server-side and not
  # exposed by any agy subcommand.
  $status = [ordered]@{ Model = $null; ResetUtc = $null; Blocked = $false; LastError = $null }

  # The two keys are not in a fixed order inside the error body, so match them independently
  # and take the last of each in the newest log that has them.
  foreach ($log in (Get-ChildItem $logDir -Filter 'cli-*.log' -ErrorAction SilentlyContinue |
      Sort-Object LastWriteTime -Descending)) {
    $blob = Get-Content $log.FullName -Raw -ErrorAction SilentlyContinue
    if ($blob -notmatch 'quotaResetTimeStamp') { continue }
    $stamps = [regex]::Matches($blob, '"quotaResetTimeStamp":\s*"([^"]+)"')
    if (-not $stamps.Count) { continue }
    $status.ResetUtc = [datetime]::Parse($stamps[$stamps.Count - 1].Groups[1].Value).ToUniversalTime()
    $status.Blocked = $status.ResetUtc -gt (Get-Date).ToUniversalTime()
    $models = [regex]::Matches($blob, '"model":\s*"([^"]+)"')
    if ($models.Count) { $status.Model = $models[$models.Count - 1].Groups[1].Value }
    $status.LastError = $log.Name
    break
  }
  [pscustomobject]$status
}

function Show-Quota {
  $q = Get-QuotaStatus
  $imgs = Get-ChildItem $brain -Recurse -Include *.jpg, *.jpeg, *.png -ErrorAction SilentlyContinue |
    Where-Object { $_.FullName -notmatch '\.tempmediaStorage' }
  $day = @($imgs | Where-Object { $_.LastWriteTime -gt (Get-Date).AddHours(-24) })

  Write-Host "image model     : $(if ($q.Model) { $q.Model } else { 'gemini-3.1-flash-image (assumed; no 429 recorded yet)' })"
  Write-Host "generated total : $($imgs.Count)"
  Write-Host "generated 24h   : $($day.Count)"
  if ($day) { Write-Host "oldest in 24h   : $((($day | Sort-Object LastWriteTime)[0]).LastWriteTime.ToString('yyyy-MM-dd HH:mm:ss'))" }
  if ($q.ResetUtc) {
    $left = $q.ResetUtc - (Get-Date).ToUniversalTime()
    Write-Host "last 429 reset  : $($q.ResetUtc.ToLocalTime().ToString('yyyy-MM-dd HH:mm:ss')) local"
    if ($q.Blocked) { Write-Host "status          : BLOCKED, $([int]$left.TotalMinutes) min left" }
    else { Write-Host 'status          : OK, quota window has reset' }
  }
  else {
    Write-Host 'status          : OK, no quota error recorded'
  }
  Write-Host 'note            : remaining allowance is server-side; agy exposes no way to query it.'
  $q
}

if ($Quota) { Show-Quota | Out-Null; return }

if (-not $Prompt -or -not $Out) { throw 'Provide -Prompt and -Out (or -Quota).' }
if ($Prompt.Count -ne $Out.Count) { throw "-Prompt has $($Prompt.Count) items but -Out has $($Out.Count)." }

$q = Get-QuotaStatus
if ($q.Blocked -and -not $Force) {
  $left = $q.ResetUtc - (Get-Date).ToUniversalTime()
  throw ("Image quota for $($q.Model) is exhausted. Resets $($q.ResetUtc.ToLocalTime().ToString('HH:mm:ss')) local " +
    "($([int]$left.TotalMinutes) min). Nothing was sent. Re-run then, or pass -Force to try anyway.")
}

$work = 0..($Prompt.Count - 1) | ForEach-Object {
  [pscustomobject]@{
    Index  = $_
    Prompt = $Prompt[$_]
    Out    = $Out[$_]
    # Unique, purely alphanumeric so agy keeps it verbatim as the filename slug. This is what
    # lets concurrent runs pick out their own image instead of racing on mtime.
    Token  = 'gi' + ([guid]::NewGuid().ToString('N').Substring(0, 10))
  }
}

$results = $work | ForEach-Object -ThrottleLimit ([Math]::Max(1, $Parallel)) -Parallel {
  $item = $_
  $brain = $using:brain
  $ratio = $using:AspectRatio
  $refs = $using:Ref
  $model = $using:Model
  $timeout = $using:TimeoutSec

  $lines = @(
    'Do NOT use run_command or any shell command. Do NOT try to move, copy or rename the file.'
    'Use ONLY the generate_image tool, exactly once, then stop.'
    "Pass image_name exactly: $($item.Token)"
  )
  if ($ratio) { $lines += "Pass aspect_ratio exactly: $ratio" }
  if ($refs) { $lines += "Pass image_paths: $($refs -join ', ')" }
  $lines += ''
  $lines += "Generate this image: $($item.Prompt)"
  $guard = $lines -join "`n"

  $since = (Get-Date).AddMinutes(-1)

  # Every `agy --print` re-authenticates on start. On a cold start that can lose the race and
  # come back with a sign-in message instead of a result. No image is spent when that happens,
  # so retry rather than fail.
  $raw = ''
  foreach ($attempt in 1..3) {
    $raw = & agy --print $guard --model $model --print-timeout "$($timeout)s" 2>&1 | Out-String
    if ($raw -notmatch '(?i)(not logged in|signing in|sign in to|log in to|authenticat\w* fail|no token|token source)') { break }
    Start-Sleep -Seconds (3 * $attempt)
  }

  $hit = Get-ChildItem $brain -Recurse -Include *.jpg, *.jpeg, *.png -ErrorAction SilentlyContinue |
    Where-Object { $_.BaseName -like "$($item.Token)*" -and $_.LastWriteTime -gt $since } |
    Sort-Object LastWriteTime -Descending | Select-Object -First 1

  if (-not $hit) {
    # Older agy builds ignore image_name. Fall back to newest untagged file from this window.
    $hit = Get-ChildItem $brain -Recurse -Include *.jpg, *.jpeg, *.png -ErrorAction SilentlyContinue |
      Where-Object { $_.LastWriteTime -gt $since -and $_.FullName -notmatch '\.tempmediaStorage' } |
      Sort-Object LastWriteTime -Descending | Select-Object -First 1
    if ($hit -and $using:Parallel -gt 1) { $hit = $null }  # unsafe to guess while others run
  }

  if (-not $hit) {
    return [pscustomobject]@{ Out = $item.Out; Path = $null; Error = ($raw.Trim()) }
  }

  $dir = Split-Path -Parent $item.Out
  if ($dir -and -not (Test-Path $dir)) { New-Item -ItemType Directory -Force $dir | Out-Null }
  if ([IO.Path]::GetExtension($item.Out) -ieq '.png') {
    Add-Type -AssemblyName System.Drawing
    $img = [System.Drawing.Image]::FromFile($hit.FullName)
    try { $img.Save($item.Out, [System.Drawing.Imaging.ImageFormat]::Png) } finally { $img.Dispose() }
  }
  else { Copy-Item $hit.FullName $item.Out -Force }

  [pscustomobject]@{ Out = $item.Out; Path = (Resolve-Path $item.Out).Path; Error = $null }
}

foreach ($r in $results) {
  if ($r.Path) { $r.Path } else { Write-Warning "FAILED $($r.Out): $($r.Error)" }
}
if ($results | Where-Object { -not $_.Path }) { exit 1 }
