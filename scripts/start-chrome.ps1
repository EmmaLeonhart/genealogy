<#
    START CHROME FOR THE PATH CAMPAIGN.

    ⛔ THE FLAGS ARE THE POINT. Chrome throttles `setTimeout` in a tab that is not on top, so a
    loop pasted into a background tab keeps every counter green and does a twentieth of the work.
    Measured 2026-09-15: `scripts/pathchains.js` managed 10 chains in 7 minutes against the 1.5s
    a chain it runs at in front -- `alive:true`, `fail:0`, every counter moving the whole time.

    The campaign runs TWO loops -- the requester and the chain fetcher -- and only one tab can be
    in front, so without these flags one of the two is always being starved. That is why this is
    a launch rule and not a debugging step: the symptom is indistinguishable from health.

    The default profile is used deliberately. Geni needs the real logged-in session and the
    collector extension, and a fresh --user-data-dir has neither.

        powershell -File scripts/start-chrome.ps1            # kills what is running first
        powershell -File scripts/start-chrome.ps1 -NoKill    # leave an existing Chrome alone
#>
param([switch]$NoKill)

$flags = @(
    '--disable-background-timer-throttling'
    '--disable-backgrounding-occluded-windows'
    '--disable-renderer-backgrounding'
    '--disable-features=CalculateNativeWinOcclusion'
    '--restore-last-session'
)

$exe = @(
    "$env:ProgramFiles\Google\Chrome\Application\chrome.exe"
    "${env:ProgramFiles(x86)}\Google\Chrome\Application\chrome.exe"
    "$env:LOCALAPPDATA\Google\Chrome\Application\chrome.exe"
) | Where-Object { Test-Path $_ } | Select-Object -First 1

if (-not $exe) { throw "chrome.exe not found in any of the usual locations" }

if (-not $NoKill) {
    # CLAUDE.md § KILL CHROME WHENEVER YOU NEED TO -- standing authority.
    Get-Process chrome -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
    # Chrome writes its session out on the way down; starting again too fast loses tabs.
    Start-Sleep -Seconds 3
}

& $exe @flags
Write-Output "started $exe with $($flags.Count) flags"
