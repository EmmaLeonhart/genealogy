# Start the download loop with no live parent, and print its PID.
#
# `Start-Process` makes the loop a child of THIS PowerShell, which then exits
# immediately -- leaving the loop orphaned. Windows does not kill orphans, so
# nothing walking a process tree from claude.exe can find it. That is the whole
# trick, and it is the difference between a download that survives the session
# and one that gets reaped every few minutes.
#
#   powershell -NoProfile -ExecutionPolicy Bypass -File scripts\wikidata-detach.ps1
#
# Progress goes to out\wikidata-loop.log. To stop it:  Stop-Process -Id <pid>

$ErrorActionPreference = 'Stop'
$loop = Join-Path $PSScriptRoot 'wikidata-loop.ps1'

$process = Start-Process -PassThru -WindowStyle Hidden `
    -FilePath 'powershell.exe' `
    -ArgumentList '-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', "`"$loop`""

Write-Output "detached loop started, pid $($process.Id)"
Write-Output 'progress: out\wikidata-loop.log     stop it: Stop-Process -Id ' + $process.Id
