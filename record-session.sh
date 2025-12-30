#!/usr/bin/env bash
# =============================================================================
#  Realistic Terminal Session — looks like actual CLI usage
# =============================================================================

# Activate venv
if [ -d ".venv" ]; then
    source .venv/bin/activate
fi

# Colors for prompt
BLUE='\033[0;34m'
GREEN='\033[0;32m'
BOLD='\033[1m'
NC='\033[0m'

# Simulates typing a command
type_cmd() {
    local cmd="$1"
    local delay="${2:-0.04}"
    
    # Show prompt
    echo -n -e "${GREEN}❯${NC} "
    
    # Type each character
    for (( i=0; i<${#cmd}; i++ )); do
        echo -n "${cmd:$i:1}"
        sleep "$delay"
    done
    echo
    sleep 0.3
}

# Run command after "typing" it
run() {
    type_cmd "$1" "${2:-0.04}"
    eval "$1"
    echo
    sleep 1
}

# Pause like reading output
pause() {
    sleep "${1:-2}"
}

# Comment (thinking out loud)
think() {
    echo -e "${BLUE}# $1${NC}"
    sleep 1
}

clear

# Session starts
echo -e "${BOLD}~/Alis-book-of-fail${NC}"
echo
sleep 1

# Step 1: Run the evaluation
think "let's run the contract suite against the staging model"
run "book-of-fail --suite contract --adapter replay"
pause 2

# Step 2: Notice failure, check the traces
think "hmm, one failed. let's see which one..."
run "ls eval/reports/latest/traces/ | head -5"
pause 1

think "checking the summary first"
run "cat eval/reports/latest/summary.json | python3 -m json.tool"
pause 2

# Step 3: Find and inspect the failing trace
think "let me find the failed case"
run "grep -l FAIL eval/reports/latest/traces/*.json"
pause 1

# Step 4: View the trace details
think "inspecting CONTRACT_0003..."
run "python3 -m eval.tools.trace_diff eval/reports/latest/traces/CONTRACT_0003_no_claimed_actions.json"
pause 3

# Step 5: Compare with baseline
think "comparing against the expected behavior"
run "python3 -m eval.tools.trace_diff eval/reports/latest/traces/CONTRACT_0003_no_claimed_actions.json --baseline eval/fixtures/baseline_traces/CONTRACT_0003_no_claimed_actions.json"
pause 3

# Step 6: Look at the raw trace
think "let me see what the model actually output"
type_cmd "cat eval/reports/latest/traces/CONTRACT_0003_no_claimed_actions.json | jq '.outputs'"
cat eval/reports/latest/traces/CONTRACT_0003_no_claimed_actions.json | python3 -c "
import json, sys
data = json.load(sys.stdin)
print(json.dumps(data.get('outputs', {}), indent=2))
"
echo
pause 2

# Step 7: Check actions
think "and confirm no actions were logged"
type_cmd "cat eval/reports/latest/traces/CONTRACT_0003_no_claimed_actions.json | jq '.actions'"
cat eval/reports/latest/traces/CONTRACT_0003_no_claimed_actions.json | python3 -c "
import json, sys
data = json.load(sys.stdin)
print(json.dumps(data.get('actions', []), indent=2))
"
echo
pause 2

# Conclusion
think "yep — model hallucinated sending an email. need to fix this."
echo
sleep 2
