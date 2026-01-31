# Move Language Basics

## Module Declaration

```move
module package_address::module_name;

use std::string::String;
use sui::object::{Self, UID};

const MY_CONST: u64 = 100;

public struct MyStruct has key, store {
    id: UID,
    value: u64,
}

public fun my_function(arg: u64): u64 { arg * 2 }
```

## Primitive Types

| Type                            | Description       |
| ------------------------------- | ----------------- |
| `bool`                          | true/false        |
| `u8, u16, u32, u64, u128, u256` | Unsigned integers |
| `address`                       | 32-byte address   |
| `vector<T>`                     | Dynamic array     |

## Variables

```move
let x: u64 = 42;
let mut y = 100;        // mutable
y = 200;
let x = 50;             // shadowing allowed
```

## Struct Definition

```move
public struct Artist {
    name: String,
}

public struct Record has key, store {
    id: UID,
    title: String,
    artist: Artist,
    year: u16,
}
```

Struct visibility: `public struct` (visible outside module), `struct` (module-only)

## Struct Operations

```move
// Create
let artist = Artist { name: b"Beatles".to_string() };

// Access fields
let n = artist.name;

// Mutate (if mut)
let mut a = Artist { name: b"X".to_string() };
a.name = b"Y".to_string();

// Unpack (required if no drop ability)
let Artist { name } = artist;
let Artist { name: _ } = artist;  // ignore field
```

## Functions

```move
// Private (default)
fun helper(): u64 { 42 }

// Public - callable from any module
public fun process(x: u64): u64 { x + 1 }

// Public entry - callable from transactions
public entry fun do_action(ctx: &mut TxContext) { }

// Entry only (not callable from other modules)
entry fun tx_only(ctx: &mut TxContext) { }
```

## References & Ownership

```move
fun take<T>(value: T) { }           // moves value
fun borrow<T>(value: &T) { }        // immutable borrow
fun borrow_mut<T>(value: &mut T) { } // mutable borrow
```

## Control Flow

```move
// if-else
if (x > 0) { x } else { 0 }

// loop
let mut i = 0;
loop {
    if (i >= 10) break;
    i = i + 1;
};

// while
while (i < 10) { i = i + 1; };

// abort
assert!(condition, ERROR_CODE);
abort ERROR_CODE
```

## Vector Operations

```move
use std::vector;

let mut v = vector::empty<u64>();
v.push_back(1);
v.push_back(2);
let len = v.length();
let first = v[0];
let popped = v.pop_back();
let exists = v.contains(&1);
```

## Option Type

```move
use std::option::{Self, Option};

let some: Option<u64> = option::some(42);
let none: Option<u64> = option::none();

if (some.is_some()) {
    let val = some.borrow();      // &T
    let val = some.extract();     // T (consumes)
}
let val = some.get_with_default(0);
```

## String Operations

```move
use std::string::String;

let s: String = b"hello".to_string();
let bytes: vector<u8> = *s.as_bytes();
let len = s.length();
s.append(b" world".to_string());
```

## Error Handling

```move
const EInvalidInput: u64 = 0;
const ENotAuthorized: u64 = 1;

public fun safe_div(a: u64, b: u64): u64 {
    assert!(b != 0, EInvalidInput);
    a / b
}
```

## Generics

```move
public struct Container<T: store> has key, store {
    id: UID,
    item: T,
}

public fun wrap<T: store>(item: T, ctx: &mut TxContext): Container<T> {
    Container { id: object::new(ctx), item }
}
```

## Abilities

| Ability | Description                                         |
| ------- | --------------------------------------------------- |
| `copy`  | Value can be copied                                 |
| `drop`  | Value can be dropped (discarded)                    |
| `store` | Value can be stored in objects                      |
| `key`   | Value is an object (requires `id: UID` first field) |

Common combinations:

- `has key, store` - Transferable object
- `has key` - Non-transferable (soulbound) object
- `has copy, drop` - Event struct
- `has store` - Embeddable in objects
