#!/bin/bash

# Automated Test Runner - Daily Testing System
# Usage: ./run_daily_tests.sh [api_url]

set -e

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
API_URL="${1:-https://tiktokshop-analyzer.com}"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
RESULTS_DIR="/tmp/test_results"
LOG_FILE="$RESULTS_DIR/test_run_${TIMESTAMP}.log"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

# Create results directory
mkdir -p "$RESULTS_DIR"

# Function to print colored output
log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $1" | tee -a "$LOG_FILE"
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}" | tee -a "$LOG_FILE"
}

log_error() {
    echo -e "${RED}❌ $1${NC}" | tee -a "$LOG_FILE"
}

log_warn() {
    echo -e "${YELLOW}⚠️  $1${NC}" | tee -a "$LOG_FILE"
}

log_info() {
    echo -e "${PURPLE}ℹ️  $1${NC}" | tee -a "$LOG_FILE"
}

# Print header
clear
echo ""
echo -e "${PURPLE}"
echo "╔════════════════════════════════════════════════════════╗"
echo "║     🤖 AUTOMATED TESTING SUITE - DAILY TESTS          ║"
echo "╚════════════════════════════════════════════════════════╝"
echo -e "${NC}"
echo ""

log "Starting automated tests..."
log "API URL: $API_URL"
log "Results Directory: $RESULTS_DIR"
log "Log File: $LOG_FILE"
echo ""

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    log_error "Python 3 is not installed or not in PATH"
    exit 1
fi

log_success "Python 3 found: $(python3 --version)"
echo ""

# Check if test suite exists
if [ ! -f "$SCRIPT_DIR/test_suite.py" ]; then
    log_error "test_suite.py not found in $SCRIPT_DIR"
    exit 1
fi

log_success "test_suite.py found"
echo ""

# Run the test suite
log_info "Running comprehensive test suite..."
echo ""

if python3 "$SCRIPT_DIR/test_suite.py" "$API_URL" 2>&1 | tee -a "$LOG_FILE"; then
    log_success "Test suite completed successfully"
else
    log_error "Test suite encountered errors"
    echo ""
    log "Checking if API is reachable..."
    if curl -s "$API_URL" > /dev/null 2>&1; then
        log_success "API is reachable"
    else
        log_error "API is NOT reachable at $API_URL"
    fi
fi

echo ""
echo ""

# Display results
if [ -f "/tmp/test_results.json" ]; then
    log_success "Test results saved to /tmp/test_results.json"
    echo ""
    log "Test Results (JSON):"
    echo "────────────────────────────────────────────────"
    python3 -m json.tool /tmp/test_results.json 2>/dev/null || cat /tmp/test_results.json
    echo "────────────────────────────────────────────────"
    echo ""
fi

if [ -f "/tmp/test_report.txt" ]; then
    log_success "Test report saved to /tmp/test_report.txt"
    echo ""
    log "Test Report:"
    echo "────────────────────────────────────────────────"
    cat /tmp/test_report.txt
    echo "────────────────────────────────────────────────"
    echo ""
fi

# Generate summary
echo ""
echo -e "${PURPLE}"
echo "╔════════════════════════════════════════════════════════╗"
echo "║                    TEST EXECUTION COMPLETE             ║"
echo "╚════════════════════════════════════════════════════════╝"
echo -e "${NC}"

log_info "Full log available at: $LOG_FILE"
log_success "All test runs archived in: $RESULTS_DIR"

# List all previous test runs
echo ""
log "Recent test runs:"
ls -lht "$RESULTS_DIR"/test_run_*.log 2>/dev/null | head -5 | awk '{print "  - " $9 " (" $6 " " $7 " " $8 ")" }'

echo ""

# Offer to display latest report
echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}"
echo "Commands to view results:"
echo ""
echo "  View latest report:  cat /tmp/test_report.txt"
echo "  View latest JSON:    cat /tmp/test_results.json"
echo "  View latest log:     tail -f $LOG_FILE"
echo "  Run tests again:     ./run_daily_tests.sh $API_URL"
echo ""
echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}"
echo ""

exit 0
