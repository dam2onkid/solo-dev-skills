module mypackage::example;

use sui::object::{Self, UID};
use sui::transfer;
use sui::tx_context::{Self, TxContext};

public struct MyObject has key, store {
    id: UID,
    value: u64,
}

fun init(ctx: &mut TxContext) {
    let obj = MyObject {
        id: object::new(ctx),
        value: 0,
    };
    transfer::transfer(obj, tx_context::sender(ctx));
}

public fun create(value: u64, recipient: address, ctx: &mut TxContext) {
    let obj = MyObject {
        id: object::new(ctx),
        value,
    };
    transfer::transfer(obj, recipient);
}

public fun create_owned(value: u64, ctx: &mut TxContext): MyObject {
    MyObject {
        id: object::new(ctx),
        value,
    }
}

public fun get_value(obj: &MyObject): u64 {
    obj.value
}

public fun set_value(obj: &mut MyObject, new_value: u64) {
    obj.value = new_value;
}

public fun destroy(obj: MyObject) {
    let MyObject { id, value: _ } = obj;
    object::delete(id);
}

#[test]
fun test_create_and_get_value() {
    use sui::test_scenario;

    let admin = @0xABCD;
    let mut scenario = test_scenario::begin(admin);

    {
        let ctx = test_scenario::ctx(&mut scenario);
        create(42, admin, ctx);
    };

    test_scenario::next_tx(&mut scenario, admin);
    {
        let obj = test_scenario::take_from_sender<MyObject>(&scenario);
        assert!(get_value(&obj) == 42, 0);
        test_scenario::return_to_sender(&scenario, obj);
    };

    test_scenario::end(scenario);
}
