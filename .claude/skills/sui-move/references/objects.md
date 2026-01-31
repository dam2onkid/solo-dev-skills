# Sui Objects & Storage

## Object Definition

Objects must have `key` ability and `id: UID` as first field.

```move
public struct MyObject has key {
    id: UID,
    value: u64,
}

public struct TransferableObject has key, store {
    id: UID,
    data: String,
}
```

## Creating Objects

```move
use sui::object;

public fun create(ctx: &mut TxContext): MyObject {
    MyObject {
        id: object::new(ctx),
        value: 100,
    }
}
```

## Storage Functions (sui::transfer)

### Transfer - Address Owned

```move
// Internal transfer (key only, same module)
transfer::transfer(obj, recipient);

// Public transfer (key + store, any module)
transfer::public_transfer(obj, recipient);
```

### Freeze - Immutable

```move
// Internal freeze
transfer::freeze_object(obj);

// Public freeze (key + store)
transfer::public_freeze_object(obj);
```

Frozen objects: accessible by immutable reference only, can never change.

### Share - Shared Object

```move
// Internal share
transfer::share_object(obj);

// Public share (key + store)
transfer::public_share_object(obj);
```

Shared objects: accessible by anyone with mutable reference.

## Ownership States

| State         | Access             | Can Transfer | Can Delete    |
| ------------- | ------------------ | ------------ | ------------- |
| Address-owned | Owner only         | Yes          | Yes           |
| Shared        | Anyone (mutable)   | No           | Yes (special) |
| Immutable     | Anyone (immutable) | No           | No            |

## TxContext

```move
use sui::tx_context::TxContext;

public fun example(ctx: &mut TxContext) {
    let sender = ctx.sender();           // transaction sender
    let epoch = ctx.epoch();             // current epoch
    let digest = ctx.digest();           // tx digest
}
```

## init Function

Special function called once when module is published.

```move
fun init(ctx: &mut TxContext) {
    let admin = AdminCap { id: object::new(ctx) };
    transfer::transfer(admin, ctx.sender());
}
```

## Object ID & UID

```move
use sui::object::{Self, UID, ID};

// Get ID from UID
let id: ID = object::uid_to_inner(&obj.id);

// Compare IDs
let same = object::id(&obj1) == object::id(&obj2);

// Delete UID (required when destroying objects)
public fun destroy(obj: MyObject) {
    let MyObject { id, value: _ } = obj;
    object::delete(id);
}
```

## Receiving Objects

For receiving objects sent to another object:

```move
use sui::transfer::Receiving;

public fun receive_item(
    parent: &mut Parent,
    item: Receiving<Item>
): Item {
    transfer::receive(&mut parent.id, item)
}
```

## Object Wrapping

Embed objects inside other objects:

```move
public struct Wrapper has key {
    id: UID,
    inner: InnerObject,  // InnerObject must have `store`
}

public fun wrap(inner: InnerObject, ctx: &mut TxContext): Wrapper {
    Wrapper { id: object::new(ctx), inner }
}

public fun unwrap(wrapper: Wrapper): InnerObject {
    let Wrapper { id, inner } = wrapper;
    object::delete(id);
    inner
}
```

## Dynamic Fields

Store heterogeneous data on objects:

```move
use sui::dynamic_field as df;

// Add field
df::add(&mut obj.id, key, value);

// Borrow field
let val: &T = df::borrow(&obj.id, key);
let val: &mut T = df::borrow_mut(&mut obj.id, key);

// Remove field
let val: T = df::remove(&mut obj.id, key);

// Check existence
let exists = df::exists_(&obj.id, key);
```

## Dynamic Object Fields

Store objects as dynamic fields (appear in explorer):

```move
use sui::dynamic_object_field as dof;

dof::add(&mut parent.id, key, child_obj);
let child: &ChildType = dof::borrow(&parent.id, key);
let child: ChildType = dof::remove(&mut parent.id, key);
```

## One-Time Witness (OTW)

Type created only once, in init, for unique setup:

```move
module example::my_token;

public struct MY_TOKEN has drop {}

fun init(witness: MY_TOKEN, ctx: &mut TxContext) {
    // witness is OTW - guaranteed to exist only here
    // Use for creating unique objects like Coin treasuries
}
```

OTW rules:

- Named after module (uppercase)
- Has only `drop` ability
- No fields
- Created only as init's first argument
