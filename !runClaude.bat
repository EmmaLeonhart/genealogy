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
