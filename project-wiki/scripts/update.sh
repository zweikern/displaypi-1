#!/usr/bin/env bash
# ============================================================
# project-wiki update
# ============================================================
# Triggers the AI agent to perform a full wiki maintenance pass.
#
# The agent will:
# 1. Read project-wiki/SCHEMA.md for conventions
# 2. Read project-wiki/index.md for the current catalog
# 3. Scan for new sources in project-wiki/sources/
# 4. Check all concept pages for staleness, orphans, contradictions
# 5. Update affected pages and cross-references
# 6. Update project-wiki/index.md
# 7. Append to project-wiki/log.md
#
# Usage: ./project-wiki update
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
WIKI_DIR="$PROJECT_ROOT/project-wiki"

echo "=== project-wiki update ==="
echo "Wiki directory: $WIKI_DIR"
echo ""
echo "The AI agent will now perform a full maintenance pass."
echo "Reference: $WIKI_DIR/SCHEMA.md"
echo ""
echo "Operations:"
echo "  1. Ingest new sources from sources/"
echo "  2. Lint all concept pages for staleness, orphans, contradictions"
echo "  3. Update cross-references"
echo "  4. Rebuild index.md"
echo "  5. Append to log.md"
echo ""
echo "Handing over to AI agent..."
echo ""

# The actual work is done by the AI agent reading SCHEMA.md.
# This script serves as the trigger and documentation.
# The agent should now proceed with the update workflow defined in SCHEMA.md.
