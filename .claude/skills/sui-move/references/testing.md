# Testing Move Code

## Test Attribute

```move
#[test]
fun test_basic() {
    let x = 2 + 2;
    assert!(x == 4, 0);
}
```

## Running Tests

```bash
sui move test                          # all tests
sui move test test_name                # filter by name
sui move test --path ./my_package      # specific package
sui move test --coverage               # with coverage
sui move test --gas-limit 1000000      # set gas limit
```

## Test Module Pattern

```move
#[test_only]
module package::my_module_tests;

use std::unit_test::assert_eq;
use package::my_module;

#[test]
fun test_feature() {
    let result = my_module::some_function();
    assert_eq!(result, expected_value);
}
```

## Assertions

```move
use std::unit_test::assert_eq;

#[test]
fun test_assertions() {
    assert!(true, 0);                    // basic assert
    assert_eq!(1, 1);                    // equality
    assert!(vector[1,2] == vector[1,2], 0);
}
```

## Expected Failure

```move
const EInvalidInput: u64 = 1;

#[test]
#[expected_failure(abort_code = EInvalidInput)]
fun test_should_fail() {
    abort EInvalidInput
}

#[test]
#[expected_failure(abort_code = 0)]
fun test_abort_zero() {
    abort 0
}

// Grouped attributes
#[test, expected_failure(abort_code = EInvalidInput)]
fun test_grouped() {
    abort EInvalidInput
}
```

## Test-Only Code

```move
// Test-only module import
#[test_only]
use std::unit_test::assert_eq;

// Test-only constant
#[test_only]
const TEST_VALUE: u64 = 42;

// Test-only function (often public for other test modules)
#[test_only]
public fun create_for_testing(ctx: &mut TxContext): MyObject {
    MyObject { id: object::new(ctx), value: 0 }
}

// Test-only struct
#[test_only]
public struct TestHelper has drop {}
```

## Testing with TxContext

```move
use sui::test_scenario::{Self as ts, Scenario};
use sui::test_utils;

#[test]
fun test_with_context() {
    let mut scenario = ts::begin(@0xALICE);

    // First transaction
    ts::next_tx(&mut scenario, @0xALICE);
    {
        let ctx = ts::ctx(&mut scenario);
        my_module::create(ctx);
    };

    // Second transaction - take object
    ts::next_tx(&mut scenario, @0xALICE);
    {
        let obj = ts::take_from_sender<MyObject>(&scenario);
        // ... use object
        ts::return_to_sender(&scenario, obj);
    };

    ts::end(scenario);
}
```

## Test Scenario Functions

```move
use sui::test_scenario as ts;

// Begin scenario with sender
let mut scenario = ts::begin(@0xALICE);

// Next transaction with sender
ts::next_tx(&mut scenario, @0xBOB);

// Get context
let ctx = ts::ctx(&mut scenario);

// Take objects
let obj = ts::take_from_sender<T>(&scenario);
let obj = ts::take_from_address<T>(&scenario, @0xALICE);
let shared = ts::take_shared<T>(&scenario);
let immutable = ts::take_immutable<T>(&scenario);

// Return objects
ts::return_to_sender(&scenario, obj);
ts::return_to_address(@0xALICE, obj);
ts::return_shared(shared);
ts::return_immutable(immutable);

// Check object existence
let has_obj = ts::has_most_recent_for_sender<T>(&scenario);
let ids = ts::ids_for_sender<T>(&scenario);

// End scenario
ts::end(scenario);
```

## Testing Shared Objects

```move
#[test]
fun test_shared_object() {
    let mut scenario = ts::begin(@0xADMIN);

    // Create and share
    ts::next_tx(&mut scenario, @0xADMIN);
    {
        let ctx = ts::ctx(&mut scenario);
        let obj = SharedObject { id: object::new(ctx), counter: 0 };
        transfer::share_object(obj);
    };

    // Use shared object
    ts::next_tx(&mut scenario, @0xUSER);
    {
        let mut shared = ts::take_shared<SharedObject>(&scenario);
        shared.counter = shared.counter + 1;
        ts::return_shared(shared);
    };

    ts::end(scenario);
}
```

## Testing Events

```move
use sui::test_scenario as ts;
use sui::event;

#[test]
fun test_events() {
    let mut scenario = ts::begin(@0xALICE);

    ts::next_tx(&mut scenario, @0xALICE);
    {
        event::emit(MyEvent { value: 42 });
    };

    // Events emitted during test can be checked via test output
    ts::end(scenario);
}
```

## Common Test Patterns

### Setup Helper

```move
#[test_only]
public fun setup(scenario: &mut Scenario) {
    ts::next_tx(scenario, @0xADMIN);
    {
        let ctx = ts::ctx(scenario);
        // Initialize state...
    };
}
```

### Test Multiple Users

```move
#[test]
fun test_multi_user() {
    let admin = @0xADMIN;
    let user1 = @0xUSER1;
    let user2 = @0xUSER2;

    let mut scenario = ts::begin(admin);

    // Admin creates
    ts::next_tx(&mut scenario, admin);
    { /* ... */ };

    // User1 interacts
    ts::next_tx(&mut scenario, user1);
    { /* ... */ };

    // User2 interacts
    ts::next_tx(&mut scenario, user2);
    { /* ... */ };

    ts::end(scenario);
}
```
