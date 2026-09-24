#!/bin/zsh
# publish_printec.sh — publish the built dashboard to the PRINTEC (Enterprise) artifact from the terminal,
# using a second stored login so no credentials are typed each time.
#
# One-time setup (you do this once, interactively):
#   CLAUDE_CONFIG_DIR="$HOME/.claude-printec" claude        # opens Claude Code in the terminal
#   /login                                                  # sign in with the PRINTEC account in the browser
#   /exit
# The Printec login then lives in ~/.claude-printec, separate from the desktop app's personal login.
#
# Every publish after that:
#   zsh ~/Downloads/BANKING/weekly-intelligence/scripts/artifact/publish_printec.sh
#
# What it does: reads the build stamp of the file, asks a headless Printec-signed Claude Code session to
# publish that exact file to the Printec artifact URL (kept as `url`, chat capability kept), and prints the
# new version number. It never touches the personal artifact.
set -e
export CLAUDE_CONFIG_DIR="$HOME/.claude-printec"
FILE="$HOME/Downloads/BANKING/weekly-intelligence/scripts/artifact/printec-dashboard.html"
URL="https://claude.ai/artifact/8a7CuDd3HCX6WQWAfbXLqA"
if [ ! -d "$CLAUDE_CONFIG_DIR" ]; then
  echo "No Printec login yet. Run once:  CLAUDE_CONFIG_DIR=\"$CLAUDE_CONFIG_DIR\" claude   then /login with the Printec account, then /exit"; exit 1
fi
if [ ! -f "$FILE" ]; then echo "Built file not found: $FILE"; exit 1; fi
STAMP=$(grep -o "build [0-9/]* [0-9:]*" "$FILE" | head -1)
SIZE=$(du -h "$FILE" | cut -f1)
echo "Publishing $FILE ($STAMP, $SIZE) to $URL with the Printec login…"
cd "$HOME/Downloads/BANKING"     # the file must sit under the session's working directory for the Artifact tool
command claude -p \
  --dangerously-skip-permissions \
  --allowedTools "Artifact,Read" \
  "Publish the file weekly-intelligence/scripts/artifact/printec-dashboard.html to the existing artifact $URL (pass that URL as url so the same artifact is updated; declare capabilities {\"sample\": {}} so the Ask the data chat keeps working; do not change favicon or title). Do nothing else. When done, reply with exactly one line: the new version number and the build stamp $STAMP."
