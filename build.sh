#!/usr/bin/env bash
# Builds the installable plugin jar: dist/wasteland-terminal-<version>.jar
# Also copies the editor scheme to dist/WastelandTerminal.icls for "Import Scheme".
# Pass --generate to regenerate src/themes/* from generate.py first.
set -euo pipefail
DIR="$(cd "$(dirname "$0")" && pwd)"
if [[ "${1:-}" == "--generate" ]]; then
  python3 "$DIR/generate.py"
fi
VERSION="$(sed -n 's:.*<version>\(.*\)</version>.*:\1:p' "$DIR/src/META-INF/plugin.xml")"
JAR="$DIR/dist/wasteland-terminal-$VERSION.jar"
rm -rf "$DIR/dist"
mkdir -p "$DIR/dist"
(cd "$DIR/src" && zip -q -r -X "$JAR" META-INF themes)
cp "$DIR/src/themes/WastelandTerminal.xml" "$DIR/dist/WastelandTerminal.icls"
echo "Built $JAR and $DIR/dist/WastelandTerminal.icls"
