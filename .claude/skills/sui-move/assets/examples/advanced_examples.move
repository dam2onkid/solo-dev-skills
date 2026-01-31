module mypackage::advanced_examples;

use sui::object::{Self, UID};
use sui::transfer;
use sui::tx_context::{Self, TxContext};
use sui::dynamic_field as df;
use sui::event;
use sui::package::{Self, Publisher};

const EFieldNotFound: u64 = 0;
const ENotAuthorized: u64 = 1;

// ============ Dynamic Fields ============

public struct Container has key {
    id: UID,
    name: vector<u8>,
}

public struct StringKey has copy, drop, store {
    key: vector<u8>,
}

public fun create_container(name: vector<u8>, ctx: &mut TxContext): Container {
    Container {
        id: object::new(ctx),
        name,
    }
}

public fun add_field<V: store>(
    container: &mut Container,
    key: vector<u8>,
    value: V
) {
    let field_key = StringKey { key };
    df::add(&mut container.id, field_key, value);
}

public fun get_field<V: store>(container: &Container, key: vector<u8>): &V {
    let field_key = StringKey { key };
    assert!(df::exists_(&container.id, field_key), EFieldNotFound);
    df::borrow(&container.id, field_key)
}

public fun get_field_mut<V: store>(container: &mut Container, key: vector<u8>): &mut V {
    let field_key = StringKey { key };
    assert!(df::exists_(&container.id, field_key), EFieldNotFound);
    df::borrow_mut(&mut container.id, field_key)
}

public fun remove_field<V: store>(container: &mut Container, key: vector<u8>): V {
    let field_key = StringKey { key };
    assert!(df::exists_(&container.id, field_key), EFieldNotFound);
    df::remove(&mut container.id, field_key)
}

public fun has_field(container: &Container, key: vector<u8>): bool {
    let field_key = StringKey { key };
    df::exists_(&container.id, field_key)
}

// ============ Events ============

public struct ItemCreated has copy, drop {
    item_id: address,
    creator: address,
    value: u64,
}

public struct ItemTransferred has copy, drop {
    item_id: address,
    from: address,
    to: address,
}

public struct TrackedItem has key, store {
    id: UID,
    value: u64,
}

public fun create_tracked_item(value: u64, ctx: &mut TxContext): TrackedItem {
    let item = TrackedItem {
        id: object::new(ctx),
        value,
    };

    event::emit(ItemCreated {
        item_id: object::uid_to_address(&item.id),
        creator: tx_context::sender(ctx),
        value,
    });

    item
}

public fun transfer_tracked_item(
    item: TrackedItem,
    recipient: address,
    ctx: &TxContext
) {
    let item_id = object::uid_to_address(&item.id);
    let from = tx_context::sender(ctx);

    event::emit(ItemTransferred {
        item_id,
        from,
        to: recipient,
    });

    transfer::public_transfer(item, recipient);
}

// ============ Generics ============

public struct Wrapper<T: store> has key, store {
    id: UID,
    content: T,
}

public fun wrap<T: store>(content: T, ctx: &mut TxContext): Wrapper<T> {
    Wrapper {
        id: object::new(ctx),
        content,
    }
}

public fun unwrap<T: store>(wrapper: Wrapper<T>): T {
    let Wrapper { id, content } = wrapper;
    object::delete(id);
    content
}

public fun borrow_content<T: store>(wrapper: &Wrapper<T>): &T {
    &wrapper.content
}

public fun borrow_content_mut<T: store>(wrapper: &mut Wrapper<T>): &mut T {
    &mut wrapper.content
}

// ============ One Time Witness (OTW) ============

public struct ADVANCED_EXAMPLES has drop {}

fun init(otw: ADVANCED_EXAMPLES, ctx: &mut TxContext) {
    let publisher: Publisher = package::claim(otw, ctx);
    transfer::public_transfer(publisher, tx_context::sender(ctx));
}

// ============ Phantom Type Parameters ============

public struct USD {}
public struct EUR {}

public struct Balance<phantom Currency> has store {
    value: u64,
}

public fun create_balance<Currency>(value: u64): Balance<Currency> {
    Balance { value }
}

public fun balance_value<Currency>(balance: &Balance<Currency>): u64 {
    balance.value
}

public fun merge_balances<Currency>(
    balance1: &mut Balance<Currency>,
    balance2: Balance<Currency>
) {
    let Balance { value } = balance2;
    balance1.value = balance1.value + value;
}

// ============ Tests ============

#[test]
fun test_dynamic_fields() {
    use sui::test_scenario;

    let admin = @0xABCD;
    let mut scenario = test_scenario::begin(admin);

    {
        let ctx = test_scenario::ctx(&mut scenario);
        let mut container = create_container(b"test", ctx);

        add_field(&mut container, b"count", 42u64);
        assert!(has_field(&container, b"count"), 0);

        let value = get_field<u64>(&container, b"count");
        assert!(*value == 42, 1);

        let removed = remove_field<u64>(&mut container, b"count");
        assert!(removed == 42, 2);
        assert!(!has_field(&container, b"count"), 3);

        transfer::transfer(container, admin);
    };

    test_scenario::end(scenario);
}

#[test]
fun test_generics() {
    use sui::test_scenario;

    let admin = @0xABCD;
    let mut scenario = test_scenario::begin(admin);

    {
        let ctx = test_scenario::ctx(&mut scenario);

        let wrapped = wrap(100u64, ctx);
        assert!(*borrow_content(&wrapped) == 100, 0);

        let value = unwrap(wrapped);
        assert!(value == 100, 1);
    };

    test_scenario::end(scenario);
}

#[test]
fun test_phantom_types() {
    let mut usd_balance = create_balance<USD>(100);
    let usd_extra = create_balance<USD>(50);

    merge_balances(&mut usd_balance, usd_extra);
    assert!(balance_value(&usd_balance) == 150, 0);

    let Balance { value: _ } = usd_balance;
}
