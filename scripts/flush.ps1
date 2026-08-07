# Commit and push the genealogical data. Safe to run on a schedule.
#
# Everything the repo collects -- GEDCOM exports, downloaded Wikidata items,
# saved Geni pages, path files, reports -- committed and pushed as it arrives,
# so a machine that hibernates or reboots never has hours of collected data
# sitting only on one disk.
#
# Run by hand with:  powershell -File scripts\flush.ps1

$ErrorActionPreference = 'Stop'
$repo = Split-Path -Parent $PSScriptRoot
Set-Location $repo

# ZIPS ARE DELIBERATELY EXCLUDED, and this is the one line in the file that
# must not be "simplified". CLAUDE.md: the zips are gitignored one explicit path
# per line so that an UNLISTED zip shows up in `git status` -- that is how Emma
# sees a new download has arrived. An automatic `git add -A` would commit the
# new zip and destroy exactly that signal. The pathspec excludes them without
# putting a *.zip pattern in .gitignore, which is separately forbidden.
$pathspec = @('--', ':(exclude)*.zip')

git add -A @pathspec

$staged = git diff --cached --name-only
if (-not $staged) {
    Write-Output 'nothing to flush'
    exit 0
}

$count = ($staged | Measure-Object -Line).Lines
$summary = ($staged | Group-Object { ($_ -split '/')[0] } |
    Sort-Object Count -Descending |
    ForEach-Object { "$($_.Name) ($($_.Count))" }) -join ', '

$msgFile = Join-Path $env:TEMP 'geni-flush-msg.txt'
$lines = @(
    "Flush: $count file(s) -- $summary",
    '',
    'Automatic commit from scripts/flush.ps1, on a schedule. Not reviewed by a',
    'human. Zips are excluded by pathspec so that an unlisted zip still shows up',
    'in git status as the signal that a download arrived.'
)
Set-Content -Path $msgFile -Value $lines -Encoding utf8
git commit -q -F $msgFile
Remove-Item $msgFile -ErrorAction SilentlyContinue

# The download tick also commits, so two git processes can occasionally want the
# index at once. A collision is transient and the next flush picks the work up,
# so retry briefly rather than treating it as a failure.
for ($attempt = 1; $attempt -le 3; $attempt++) {
    git push -q
    if ($LASTEXITCODE -eq 0) {
        Write-Output "flushed $count file(s): $summary"
        exit 0
    }
    Start-Sleep -Seconds 10
}

Write-Output "committed $count file(s) but the push failed three times; the next flush will carry it"
exit 1
