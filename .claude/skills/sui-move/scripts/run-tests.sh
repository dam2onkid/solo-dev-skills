#!/bin/bash
# Sui Move Test Runner
# Usage: ./run-tests.sh [filter] [options]

set -e

COVERAGE=false
WATCH=false
VERBOSE=false
GAS_LIMIT=""
PKG_PATH="."
FILTER=""

show_help() {
    cat << 'EOF'
Sui Move Test Runner

Usage: ./run-tests.sh [filter] [options]

Options:
  -c, --coverage      Generate coverage report
  -w, --watch         Watch mode - re-run on changes
  -v, --verbose       Verbose output
  -g, --gas-limit N   Set gas limit
  -p, --path PATH     Package path (default: auto-detect)
  -h, --help          Show help

Examples:
  ./run-tests.sh                       # Run all tests
  ./run-tests.sh test_create           # Filter by name
  ./run-tests.sh --coverage            # With coverage
  ./run-tests.sh test_mint --watch     # Watch mode
  ./run-tests.sh -c -v                 # Coverage + verbose
EOF
}

find_package_path() {
    if [[ -f "$PKG_PATH/Move.toml" ]]; then
        echo "$PKG_PATH"
    elif [[ -f "Move.toml" ]]; then
        echo "."
    else
        local dir=$(find . -maxdepth 2 -name "Move.toml" -exec dirname {} \; 2>/dev/null | head -1)
        echo "${dir:-.}"
    fi
}

run_tests() {
    local cmd="sui move test"

    [[ -n "$FILTER" ]] && cmd="$cmd $FILTER"
    cmd="$cmd --path $PKG_PATH"
    [[ "$COVERAGE" == true ]] && cmd="$cmd --coverage"
    [[ -n "$GAS_LIMIT" ]] && cmd="$cmd --gas-limit $GAS_LIMIT"

    echo ""
    echo "============================================================"
    echo "Running Move Tests"
    echo "============================================================"

    if [[ "$VERBOSE" == true ]]; then
        echo "Command: $cmd"
        echo "Path: $PKG_PATH"
        [[ -n "$FILTER" ]] && echo "Filter: $FILTER"
        [[ "$COVERAGE" == true ]] && echo "Coverage: enabled"
    fi

    echo ""

    local start=$(date +%s)

    if $cmd; then
        local end=$(date +%s)
        echo ""
        echo "✅ Tests completed in $((end - start))s"
        return 0
    else
        local end=$(date +%s)
        echo ""
        echo "❌ Tests failed after $((end - start))s"
        return 1
    fi
}

watch_mode() {
    echo ""
    echo "👀 Watch mode enabled. Watching for .move file changes..."
    echo "   Press Ctrl+C to stop"
    echo ""

    run_tests || true
    echo ""
    echo "👀 Watching for changes..."

    local sources_dir="$PKG_PATH/sources"
    local tests_dir="$PKG_PATH/tests"

    if command -v fswatch &> /dev/null; then
        fswatch -o "$sources_dir" "$tests_dir" 2>/dev/null | while read; do
            clear
            run_tests || true
            echo ""
            echo "👀 Watching for changes..."
        done
    elif command -v inotifywait &> /dev/null; then
        while true; do
            inotifywait -q -e modify -r "$sources_dir" "$tests_dir" 2>/dev/null
            clear
            run_tests || true
            echo ""
            echo "👀 Watching for changes..."
        done
    else
        echo "Watch mode requires 'fswatch' (macOS) or 'inotifywait' (Linux)"
        echo "Install with: brew install fswatch (macOS) or apt install inotify-tools (Linux)"
        exit 1
    fi
}

# Parse arguments
while [[ $# -gt 0 ]]; do
    case "$1" in
        -c|--coverage) COVERAGE=true; shift ;;
        -w|--watch) WATCH=true; shift ;;
        -v|--verbose) VERBOSE=true; shift ;;
        -g|--gas-limit) GAS_LIMIT="$2"; shift 2 ;;
        -p|--path) PKG_PATH="$2"; shift 2 ;;
        -h|--help) show_help; exit 0 ;;
        -*) echo "Unknown option: $1"; show_help; exit 1 ;;
        *) FILTER="$1"; shift ;;
    esac
done

PKG_PATH=$(find_package_path)

if [[ ! -f "$PKG_PATH/Move.toml" ]]; then
    echo "Error: No Move.toml found. Are you in a Move package directory?"
    exit 1
fi

if [[ "$WATCH" == true ]]; then
    watch_mode
else
    run_tests
fi
