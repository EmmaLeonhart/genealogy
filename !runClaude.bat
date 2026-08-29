@echo off
setlocal EnableExtensions

REM ---------------------------------------------------------------
REM !runClaude.bat - launch Claude Code in this repo, NON-elevated.
REM
REM Manual double-click entry point. Same BOOT_PROMPT as startclaude.bat
REM (the logon launcher) but with no 15-second wait.
REM
REM This used to be three lines ending in a bare "claude", which gives an
REM IDLE session - and an idle session writes NO transcript, because the
REM .jsonl under %USERPROFILE%\.claude\projects\ is created on the first
REM exchange, not at launch. Passing a prompt is what fixes that.
REM Do NOT add --no-session-persistence; that is what actually suppresses
REM transcripts.
REM ---------------------------------------------------------------

cd /d "%~dp0"

title Claude Code - geni

echo ===============================================================
echo  Claude Code - geni (NOT elevated)
echo  Working dir: %CD%
echo  Context:     CLAUDE.md in this folder
echo ===============================================================
echo.

REM %USERPROFILE% is NOT guaranteed to be set. PowerShell's
REM Start-Process -UseNewEnvironment rebuilds the block from the registry, and
REM on this machine that block is DEGENERATE: USERPROFILE empty, SystemDrive
REM empty, USERNAME=SYSTEM, and System32 off PATH (even findstr is missing).
REM Measured 2026-08-28. Do NOT start this script that way. Use explorer.exe,
REM which also strips the CLAUDE_CODE_* child-session vars but keeps the real
REM logon environment:   Start-Process explorer.exe '"<full path to this .bat>"'
if not defined USERPROFILE (
    if defined HOMEDRIVE if defined HOMEPATH set "USERPROFILE=%HOMEDRIVE%%HOMEPATH%"
)
if not defined USERPROFILE if defined SystemDrive set "USERPROFILE=%SystemDrive%\Users\%USERNAME%"
if not exist "%USERPROFILE%\" (
    echo ERROR: degenerate environment - USERPROFILE could not be resolved.
    echo Start this from the Startup shortcut, Explorer, or a normal console.
    pause
    exit /b 1
)

set "CLAUDE_EXE="
where claude >nul 2>&1
if %errorlevel% equ 0 (
    set "CLAUDE_EXE=claude"
) else if exist "%USERPROFILE%\.local\bin\claude.exe" (
    set "CLAUDE_EXE=%USERPROFILE%\.local\bin\claude.exe"
) else (
    echo ERROR: claude.exe not found on PATH or in %USERPROFILE%\.local\bin
    echo Install Claude Code, or edit this script with the correct path.
    pause
    exit /b 1
)

set "BOOT_PROMPT=Read queue.md and start working the highest-priority item that is not blocked on user action. Follow the queue-driven-workflow skill: finish an item, delete it from queue.md, append a dated devlog.md entry in the same commit, then push. Ask me before anything destructive."

"%CLAUDE_EXE%" "%BOOT_PROMPT%"

echo.
echo Claude Code exited with code %errorlevel%.
pause
