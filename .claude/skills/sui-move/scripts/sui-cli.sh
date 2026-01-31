#!/bin/bash
# Sui Move CLI Helper
# Usage: ./sui-cli.sh <command> [args...]

set -e

DEFAULT_GAS_BUDGET="100000000"

show_help() {
    cat << 'EOF'
Sui Move CLI Helper

Commands:
  new <name>              Create new Move package
  build [path]            Build package
  test [filter] [path]    Run tests
  test:coverage [path]    Run tests with coverage
  publish [path]          Publish to network
  publish:dry [path]      Dry-run publish
  call <pkg> <mod> <fn>   Call Move function
  objects [address]       List owned objects
  object <id>             Get object details
  gas                     Check gas balance
  faucet                  Request testnet SUI
  address                 Show active address
  switch <env>            Switch network (devnet|testnet|mainnet)
  envs                    List environments

Examples:
  ./sui-cli.sh new my_project
  ./sui-cli.sh build
  ./sui-cli.sh test test_create
  ./sui-cli.sh publish
  ./sui-cli.sh call 0x... my_module my_function 100
EOF
}

find_package_path() {
    local provided="$1"
    if [[ -n "$provided" ]]; then
        echo "$provided"
    elif [[ -f "Move.toml" ]]; then
        echo "."
    else
        local dirs=$(find . -maxdepth 2 -name "Move.toml" -exec dirname {} \; 2>/dev/null | head -1)
        if [[ -n "$dirs" ]]; then
            echo "$dirs"
        else
            echo "."
        fi
    fi
}

cmd_new() {
    local name="$1"
    if [[ -z "$name" ]]; then
        echo "Usage: sui-cli.sh new <package-name>"
        exit 1
    fi
    sui move new "$name"
    echo ""
    echo "Package '$name' created!"
    echo "Next: cd $name && sui move build"
}

cmd_build() {
    local path=$(find_package_path "$1")
    sui move build --path "$path"
}

cmd_test() {
    local filter="$1"
    local path=$(find_package_path "$2")
    if [[ -n "$filter" && ! "$filter" =~ ^- ]]; then
        sui move test "$filter" --path "$path"
    else
        sui move test --path "$path"
    fi
}

cmd_test_coverage() {
    local path=$(find_package_path "$1")
    sui move test --coverage --path "$path"
}

cmd_publish() {
    local path=$(find_package_path "$1")
    sui client publish --path "$path" --gas-budget "$DEFAULT_GAS_BUDGET"
}

cmd_publish_dry() {
    local path=$(find_package_path "$1")
    sui client publish --path "$path" --gas-budget "$DEFAULT_GAS_BUDGET" --dry-run
}

cmd_call() {
    local pkg="$1"
    local mod="$2"
    local fn="$3"
    shift 3 || true

    if [[ -z "$pkg" || -z "$mod" || -z "$fn" ]]; then
        echo "Usage: sui-cli.sh call <package-id> <module> <function> [args...]"
        exit 1
    fi

    local args_str=""
    if [[ $# -gt 0 ]]; then
        args_str="--args $*"
    fi

    sui client call --package "$pkg" --module "$mod" --function "$fn" $args_str --gas-budget "$DEFAULT_GAS_BUDGET"
}

cmd_objects() {
    if [[ -n "$1" ]]; then
        sui client objects --address "$1"
    else
        sui client objects
    fi
}

cmd_object() {
    if [[ -z "$1" ]]; then
        echo "Usage: sui-cli.sh object <object-id>"
        exit 1
    fi
    sui client object "$1"
}

cmd_gas() {
    sui client gas
}

cmd_faucet() {
    sui client faucet
}

cmd_address() {
    sui client active-address
}

cmd_switch() {
    local env="$1"
    if [[ ! "$env" =~ ^(devnet|testnet|mainnet|localnet)$ ]]; then
        echo "Usage: sui-cli.sh switch <devnet|testnet|mainnet|localnet>"
        exit 1
    fi
    sui client switch --env "$env"
}

cmd_envs() {
    sui client envs
}

case "${1:-help}" in
    new)           cmd_new "$2" ;;
    build)         cmd_build "$2" ;;
    test)          cmd_test "$2" "$3" ;;
    test:coverage) cmd_test_coverage "$2" ;;
    publish)       cmd_publish "$2" ;;
    publish:dry)   cmd_publish_dry "$2" ;;
    call)          shift; cmd_call "$@" ;;
    objects)       cmd_objects "$2" ;;
    object)        cmd_object "$2" ;;
    gas)           cmd_gas ;;
    faucet)        cmd_faucet ;;
    address)       cmd_address ;;
    switch)        cmd_switch "$2" ;;
    envs)          cmd_envs ;;
    help|--help|-h) show_help ;;
    *)             echo "Unknown command: $1"; show_help; exit 1 ;;
esac
