# Common Move Patterns

## Capability Pattern

Gate functions with capability objects:

```move
public struct AdminCap has key, store { id: UID }

fun init(ctx: &mut TxContext) {
    transfer::transfer(
        AdminCap { id: object::new(ctx) },
        ctx.sender()
    );
}

public fun admin_only(_: &AdminCap, /* other args */) {
    // Only AdminCap holder can call
}
```

## Witness Pattern

Prove type authenticity:

```move
public struct WITNESS has drop {}

public fun create_with_witness<T: drop>(_witness: T): SomeType {
    // T proves caller has access to the module that defines T
}

// Usage:
create_with_witness(WITNESS {})
```

## One-Time Witness (OTW)

Unique witness for one-time initialization:

```move
module example::my_coin;

public struct MY_COIN has drop {}

fun init(witness: MY_COIN, ctx: &mut TxContext) {
    // Create treasury, register type, etc.
    // MY_COIN can never be created again
}
```

## Publisher Pattern

Prove package publisher:

```move
use sui::package::{Self, Publisher};

public struct MY_MODULE has drop {}

fun init(otw: MY_MODULE, ctx: &mut TxContext) {
    let publisher = package::claim(otw, ctx);
    transfer::public_transfer(publisher, ctx.sender());
}

public fun publisher_only(pub: &Publisher) {
    assert!(package::from_module<MY_MODULE>(pub), ENotPublisher);
}
```

## Hot Potato Pattern

Force function call sequence:

```move
// No abilities = must be consumed
public struct Receipt { amount: u64 }

public fun start_action(): Receipt {
    Receipt { amount: 100 }
}

public fun complete_action(receipt: Receipt) {
    let Receipt { amount: _ } = receipt;  // Consumed here
}

// Usage: Must call complete_action after start_action
// let receipt = start_action();
// complete_action(receipt);  // Must happen or compile error
```

## Request Pattern

Multi-step authorization:

```move
public struct WithdrawRequest {
    amount: u64,
    requester: address,
}

public fun request_withdraw(amount: u64, ctx: &TxContext): WithdrawRequest {
    WithdrawRequest { amount, requester: ctx.sender() }
}

public fun approve_withdraw(
    _: &AdminCap,
    request: WithdrawRequest,
    vault: &mut Vault
) {
    let WithdrawRequest { amount, requester } = request;
    // Process withdrawal...
}
```

## Object Pool Pattern

Reusable shared objects:

```move
public struct Pool has key {
    id: UID,
    items: vector<Item>,
}

public fun borrow(pool: &mut Pool): Item {
    pool.items.pop_back()
}

public fun return_item(pool: &mut Pool, item: Item) {
    pool.items.push_back(item);
}
```

## Registry Pattern

Map addresses/names to objects:

```move
use sui::table::{Self, Table};

public struct Registry has key {
    id: UID,
    records: Table<String, address>,
}

public fun register(
    registry: &mut Registry,
    name: String,
    addr: address
) {
    table::add(&mut registry.records, name, addr);
}

public fun lookup(registry: &Registry, name: String): address {
    *table::borrow(&registry.records, name)
}
```

## Collection Patterns

### Table (Key-Value Store)

```move
use sui::table::{Self, Table};

public struct Data has key {
    id: UID,
    items: Table<address, u64>,
}

// Operations
table::add(&mut t, key, value);
table::borrow(&t, key);
table::borrow_mut(&mut t, key);
table::remove(&mut t, key);
table::contains(&t, key);
table::length(&t);
```

### ObjectTable (Object Values)

```move
use sui::object_table::{Self, ObjectTable};

public struct Container has key {
    id: UID,
    objects: ObjectTable<ID, ChildObject>,
}
```

### Bag (Heterogeneous)

```move
use sui::bag::{Self, Bag};

public struct Mixed has key {
    id: UID,
    data: Bag,
}

// Can store different types with different keys
bag::add(&mut b, b"count", 42u64);
bag::add(&mut b, b"name", b"test".to_string());
```

### VecMap (Small Collections)

```move
use sui::vec_map::{Self, VecMap};

let mut map = vec_map::empty<String, u64>();
vec_map::insert(&mut map, key, value);
```

## Error Handling Pattern

```move
const ENotOwner: u64 = 0;
const EInsufficientBalance: u64 = 1;
const EAlreadyExists: u64 = 2;

public fun transfer_funds(
    from: &mut Account,
    to: &mut Account,
    amount: u64,
    ctx: &TxContext
) {
    assert!(from.owner == ctx.sender(), ENotOwner);
    assert!(from.balance >= amount, EInsufficientBalance);

    from.balance = from.balance - amount;
    to.balance = to.balance + amount;
}
```

## Event Emission

```move
use sui::event;

public struct TransferEvent has copy, drop {
    from: address,
    to: address,
    amount: u64,
}

public fun transfer(from: address, to: address, amount: u64) {
    // ... transfer logic ...

    event::emit(TransferEvent { from, to, amount });
}
```

## Clock Usage

```move
use sui::clock::{Self, Clock};

public fun time_sensitive(clock: &Clock) {
    let now_ms = clock::timestamp_ms(clock);
    // Use timestamp for time-based logic
}
```

Clock is a shared object at `0x6`, pass as argument in transactions.

## Coin Operations

```move
use sui::coin::{Self, Coin};
use sui::sui::SUI;

public fun process_payment(
    payment: Coin<SUI>,
    ctx: &mut TxContext
): Coin<SUI> {
    let value = coin::value(&payment);

    // Split
    let portion = coin::split(&mut payment, value / 2, ctx);

    // Merge
    coin::join(&mut payment, portion);

    payment
}
```
