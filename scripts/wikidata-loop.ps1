# Run download ticks back to back until the queue is empty.
#
# **Why this exists, measured rather than assumed.** Every download started from
# inside the Claude session was a descendant of claude.exe:
#
#     python -m genimerge wikidata-download
#       <- powershell.exe <- bash.exe <- bash.exe <- bash.exe <- claude.exe
#
# so whenever the harness reaped a background task it took the download with it.
# The run was being killed every few minutes by the thing supervising it. Launch
# this with scripts/wikidata-detach.ps1 and it has no live parent, so there is no
# tree for anything to kill.
#
# It is still not immortal: a reboot ends it, and only a Windows scheduled task
# survives that. It covers the case that was actually biting.
#
# Safe to start more than once -- the heartbeat lock means a second loop's ticks
# do nothing until the first stops.
#
# **Never `tail -f` out\wikidata-loop.log.** Git's MSYS tail.exe opens the file
# without sharing write access, so `Add-Content` below starts failing and
# $ErrorActionPreference = 'Continue' swallows the error: the loop keeps ticking
# and downloading, and logs nothing at all. It looks exactly like a dead job.
# Measured 2026-08-08 -- an hour of silent log with 88,000 items downloaded
# underneath it, and the blocked line appeared the second tail was killed.
# To watch progress, read the sqlite index instead; it takes no lock on this
# file:
#     python -c "import sys; sys.path.insert(0,'src'); from genimerge import wikidownload; print(wikidownload.StateIndex('out/wikidata/download-state.sqlite3').counts())"

$ErrorActionPreference = 'Continue'
$repo = Split-Path -Parent $PSScriptRoot
Set-Location $repo

$python = 'C:\Program Files\Python313\python.exe'
$log = Join-Path $repo 'out\wikidata-loop.log'
New-Item -ItemType Directory -Force -Path (Split-Path $log) | Out-Null

function Write-Log($message) {
    $stamp = Get-Date -Format 'yyyy-MM-dd HH:mm:ss'
    Add-Content -Path $log -Value "$stamp  $message" -Encoding utf8
}

Write-Log "loop started, pid $PID"

while ($true) {
    $counts = & $python -c "import sys; sys.path.insert(0, 'src'); from genimerge import wikidownload; c = wikidownload.StateIndex('out/wikidata/download-state.sqlite3').counts(); print('{}|{}'.format(c.get('done', 0), c.get('queued', 0)))"
    $parts = $counts -split '\|'
    $queued = [int]$parts[1]

    if ($queued -le 0) {
        Write-Log "queue empty at $($parts[0]) stored -- loop finished"
        break
    }

    Write-Log "tick: $($parts[0]) stored, $queued queued"
    & powershell -NoProfile -ExecutionPolicy Bypass -File (Join-Path $PSScriptRoot 'wikidata-tick.ps1') 2>&1 |
        ForEach-Object { Write-Log "  $_" }

    # A tick that declined on the lock returns at once; without a pause the loop
    # would spin. A tick that did work has already used its eleven minutes.
    Start-Sleep -Seconds 30
}

Write-Log 'loop exiting'
