# One tick of the Wikidata download.
#
# Emma's machine interrupts the download constantly, so resumability alone is
# not enough -- something has to notice and start it again. That is this script,
# fired on a schedule. It is written to be safe to run at any moment, including
# while a download is already going: `wikidata-download` takes a heartbeat lock
# and a second copy exits immediately rather than appending to the same shard.
#
# Each tick runs a bounded chunk rather than the whole job, so a tick always
# ends and the shards get committed on a regular cadence instead of only at the
# end of a four-hour run. An interrupted tick loses at most the batch in flight.
#
# Run by hand with:  powershell -File scripts\wikidata-tick.ps1

$ErrorActionPreference = 'Stop'
$repo = Split-Path -Parent $PSScriptRoot
Set-Location $repo

$python = 'C:\Program Files\Python313\python.exe'
$env:PYTHONPATH = 'src'

# ~20,000 items is about eleven minutes at the observed 29.5/s. Sized to fit
# inside a fifteen-minute schedule with room for the commit and push.
& $python -u -m genimerge wikidata-download --limit 20000 --report-every 100
$exit = $LASTEXITCODE

# Commit whatever landed, whether or not the chunk finished cleanly -- a tick
# that tripped the circuit breaker still stored everything up to the outage.
$pending = git status --porcelain -- wikidata/items
if ($pending) {
    $held = & $python -c "import sys; sys.path.insert(0, 'src'); from genimerge import wikidownload; i = wikidownload.StateIndex('out/wikidata/download-state.sqlite3'); c = i.counts(); print('{} stored, {} queued'.format(c.get('done', 0), c.get('queued', 0)))"

    # A message file, not `-m` and not a here-string piped to `-F -`: PowerShell
    # 5.1 has no heredoc, and CLAUDE.md records that it mangles < and > in
    # native-command arguments even inside quotes.
    $msgFile = Join-Path $env:TEMP 'wikidata-tick-msg.txt'
    $lines = @(
        "Wikidata download: $held",
        '',
        'Automatic tick from scripts/wikidata-tick.ps1. Not reviewed by a human;',
        "the numbers are the download's own index counting itself."
    )
    Set-Content -Path $msgFile -Value $lines -Encoding utf8

    git add wikidata/items
    git commit -q -F $msgFile
    git push -q
    Remove-Item $msgFile -ErrorAction SilentlyContinue
    Write-Output "committed and pushed: $held"
} else {
    Write-Output 'no new shards this tick'
}

exit $exit
