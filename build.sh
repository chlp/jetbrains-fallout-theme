#!/usr/bin/env bash
# Builds the installable plugin jar: jetbrains/dist/fallout-theme.jar
# Also copies the editor scheme to dist/Fallout.icls for "Import Scheme".
set -euo pipefail
DIR="$(cd "$(dirname "$0")" && pwd)"
if [[ "${1:-}" == "--generate" ]]; then
  python3 "$DIR/generate.py"
fi
rm -rf "$DIR/dist"
mkdir -p "$DIR/dist"
(cd "$DIR/src" && zip -q -r -X "$DIR/dist/fallout-theme.jar" META-INF themes)
cp "$DIR/src/themes/Fallout.xml" "$DIR/dist/Fallout.icls"
echo "Built $DIR/dist/fallout-theme.jar and $DIR/dist/Fallout.icls"
