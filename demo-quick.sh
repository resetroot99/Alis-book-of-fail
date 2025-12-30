#!/usr/bin/env bash
# =============================================================================
#  Ali's Book of Fail — Quick Demo (no delays, for testing)
# =============================================================================

# Activate venv if it exists
if [ -d ".venv" ]; then
    source .venv/bin/activate
fi

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
BOLD='\033[1m'
DIM='\033[2m'
NC='\033[0m'

echo
echo -e "${BOLD}${MAGENTA}Ali's Book of Fail — Quick Demo${NC}"
echo -e "${DIM}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo

# Run suite
echo -e "${CYAN}▸ Running contract suite...${NC}"
set +e
python3 -m eval.harness.cli --suite contract --adapter replay --out eval/reports/demo 2>&1
set -e
echo

# Show failing case
echo -e "${CYAN}▸ Failing case details:${NC}"
python3 -m eval.tools.trace_diff eval/reports/demo/traces/CONTRACT_0003_no_claimed_actions.json 2>&1
echo

# Show summary
echo -e "${CYAN}▸ Summary:${NC}"
cat eval/reports/demo/summary.json | python3 -m json.tool
echo

echo -e "${GREEN}✓ Demo complete${NC}"
