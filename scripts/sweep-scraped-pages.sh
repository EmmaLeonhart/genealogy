#!/usr/bin/env bash
# Move blob-saved Geni profile pages out of Downloads into geni-scraping/.
#
# The pages are saved by the browser from the page itself — a Blob of
# `document.documentElement.outerHTML` with `<geni id>.html` as the download name —
# so the HTML never passes through the agent's context. See geni-scraping/README.md.
#
# Refuses to overwrite: a page already saved stays as it was.
set -euo pipefail
DL="/c/Users/Emma/Downloads"
DEST="geni-scraping"
n=0; skip=0
shopt -s nullglob
for f in "$DL"/6*.html; do
  b=$(basename "$f")
  if [ -e "$DEST/$b" ]; then rm -f "$f"; skip=$((skip+1)); continue; fi
  mv "$f" "$DEST/$b"; n=$((n+1))
done
echo "swept $n new, $skip already held; geni-scraping now $(ls "$DEST"/*.html 2>/dev/null | wc -l)"
