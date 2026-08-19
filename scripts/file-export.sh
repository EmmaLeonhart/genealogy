#!/usr/bin/env bash
# File a freshly downloaded Geni export into exports/chain-seeds/, safely.
#
# The bug this exists to stop, 2026-08-19: the loop filed "the newest zip in
# Downloads" straight after clicking download. When the download had NOT landed
# -- Geni's /download/task/<id> link 404s if the build is not actually finished,
# and the "ready" text can be read off a stale render -- the newest zip was the
# PREVIOUS export, so one export got filed twice under two different seed names.
# Byte-identical, caught by sha256, untracked, removed. It would have been a
# tracked duplicate one commit later.
#
#   scripts/file-export.sh <seed-id> <baseline-zip-name>
#
# baseline-zip-name is the newest zip BEFORE the download was triggered. If the
# newest zip still equals it, nothing has arrived and this refuses to file.
set -euo pipefail
SEED="$1"; BASE="$2"
DL="/c/Users/Emma/Downloads"
DEST="exports/chain-seeds/export-Forest-${SEED}.ged"
NEW=$(ls -t "$DL"/*.zip | head -1)
if [ "$(basename "$NEW")" = "$BASE" ]; then
  echo "NOT-ARRIVED: newest zip is still $BASE"; exit 1
fi
if [ -e "$DEST" ]; then
  echo "REFUSING: $DEST already exists"; exit 1
fi
T=exports/chain-seeds/_t
rm -rf "$T"; mkdir -p "$T"
unzip -o -q "$NEW" -d "$T"
G=$(ls "$T"/*.ged | head -1)
mv "$G" "$DEST"; rmdir "$T"
echo "filed $DEST  $(grep -c '^0 @I' "$DEST") people  from $(basename "$NEW")"
