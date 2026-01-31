---
name: sui-move
description: Write and test Move smart contracts on Sui blockchain. Use when creating new Move packages, defining modules/structs/functions, implementing objects with key/store abilities, using storage functions (transfer, share, freeze), writing unit tests with test_scenario, implementing patterns (capability, witness, OTW, hot potato), working with collections (Table, Bag, VecMap), handling Coins, emitting events, or debugging Move code.
---

# Sui Move Smart Contracts

Write, test, and deploy Move smart contracts on the Sui blockchain.

## Quick Start

```bash
sui move new my_package        # create package
sui move build                 # compile
sui move test                  # run tests
sui client publish --gas-budget 100000000  # deploy
```

## Package Structure

```
my_package/
├── Move.toml          # manifest
├── sources/
│   └── my_module.move # source files
└── tests/
    └── my_module_tests.move
```

## Move.toml

```toml
[package]
name = "my_package"
edition = "2024.beta"

[dependencies]
Sui = { git = "https://github.com/MystenLabs/sui.git", subdir = "crates/sui-framework/packages/sui-framework", rev = "framework/testnet" }

[addresses]
my_package = "0x0"
```

## Basic Module Template

```move
module my_package::my_module;

use std::string::String;
use sui::event;

const ENotAuthorized: u64 = 0;

public struct AdminCap has key, store { id: UID }

public struct Item has key, store {
    id: UID,
    name: String,
    value: u64,
}

public struct ItemCreated has copy, drop {
    item_id: ID,
    creator: address,
}

fun init(ctx: &mut TxContext) {
    transfer::transfer(
        AdminCap { id: object::new(ctx) },
        ctx.sender()
    );
}

public fun create_item(
    name: String,
    value: u64,
    ctx: &mut TxContext
): Item {
    let item = Item {
        id: object::new(ctx),
        name,
        value,
    };

    event::emit(ItemCreated {
        item_id: object::id(&item),
        creator: ctx.sender(),
    });

    item
}

public fun transfer_item(item: Item, recipient: address) {
    transfer::public_transfer(item, recipient);
}
```

## Basic Test Template

```move
#[test_only]
module my_package::my_module_tests;

use std::unit_test::assert_eq;
use sui::test_scenario as ts;
use my_package::my_module::{Self, Item, AdminCap};

#[test]
fun test_create_item() {
    let admin = @0xADMIN;
    let mut scenario = ts::begin(admin);

    // init called automatically, take AdminCap
    ts::next_tx(&mut scenario, admin);
    {
        let cap = ts::take_from_sender<AdminCap>(&scenario);
        ts::return_to_sender(&scenario, cap);
    };

    // Create item
    ts::next_tx(&mut scenario, admin);
    {
        let ctx = ts::ctx(&mut scenario);
        let item = my_module::create_item(
            b"Test".to_string(),
            100,
            ctx
        );
        transfer::public_transfer(item, admin);
    };

    // Verify item
    ts::next_tx(&mut scenario, admin);
    {
        let item = ts::take_from_sender<Item>(&scenario);
        // assertions...
        ts::return_to_sender(&scenario, item);
    };

    ts::end(scenario);
}
```

## References

- [Language Basics](references/basics.md) - Types, structs, functions, modules, abilities
- [Objects & Storage](references/objects.md) - UID, transfer, share, freeze, dynamic fields
- [Testing](references/testing.md) - test_scenario, assertions, expected_failure
- [Patterns](references/patterns.md) - Capability, witness, OTW, hot potato, collections

## Scripts

### CLI Helper (`scripts/sui-cli.sh`)

```bash
./scripts/sui-cli.sh new my_package      # create package
./scripts/sui-cli.sh build               # compile
./scripts/sui-cli.sh test                # run all tests
./scripts/sui-cli.sh test test_create    # filtered tests
./scripts/sui-cli.sh publish             # deploy to network
./scripts/sui-cli.sh call <pkg> <mod> <fn> [args...]
./scripts/sui-cli.sh objects             # list owned objects
./scripts/sui-cli.sh gas                 # check balance
./scripts/sui-cli.sh faucet              # request testnet SUI
./scripts/sui-cli.sh switch testnet      # switch network
./scripts/sui-cli.sh help                # all commands
```

### Test Runner (`scripts/run-tests.sh`)

```bash
./scripts/run-tests.sh                   # run all tests
./scripts/run-tests.sh test_mint         # filter by name
./scripts/run-tests.sh --coverage        # with coverage
./scripts/run-tests.sh --watch           # watch mode
./scripts/run-tests.sh test_x -w -v      # filter + watch + verbose
```

## Example Templates

Copy from `assets/examples/` to bootstrap projects:

- `basic_module.move` - Simple object with CRUD, init, tests
- `ownership_examples.move` - Address-owned, shared, immutable, capability
- `test_examples.move` - Unit tests, expected_failure, multi-user, shared objects
- `advanced_examples.move` - Dynamic fields, events, generics, OTW, phantom types

## Raw CLI Commands

```bash
sui move new <name>                    # new package
sui move build                         # compile
sui move test                          # all tests
sui move test <filter>                 # filtered tests
sui move test --coverage               # with coverage
sui client publish --gas-budget <n>    # deploy to network
sui client call --package <pkg> --module <mod> --function <fn> --args <args>
```

## External Resources

- [The Move Book](https://move-book.com)
- [Sui Move Examples](https://github.com/MystenLabs/sui/tree/main/examples)
- [Sui Framework Source](https://github.com/MystenLabs/sui/tree/main/crates/sui-framework)
