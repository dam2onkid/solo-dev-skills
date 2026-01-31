module mypackage::ownership_examples;

use sui::object::{Self, UID};
use sui::transfer;
use sui::tx_context::{Self, TxContext};

// ============ Address-Owned Objects ============

public struct OwnedObject has key, store {
    id: UID,
    data: vector<u8>,
}

public fun create_owned(data: vector<u8>, recipient: address, ctx: &mut TxContext) {
    let obj = OwnedObject {
        id: object::new(ctx),
        data,
    };
    transfer::transfer(obj, recipient);
}

public fun transfer_owned(obj: OwnedObject, new_owner: address) {
    transfer::transfer(obj, new_owner);
}

// ============ Shared Objects ============

public struct SharedConfig has key {
    id: UID,
    value: u64,
    admin: address,
}

public fun create_shared_config(value: u64, ctx: &mut TxContext) {
    let config = SharedConfig {
        id: object::new(ctx),
        value,
        admin: tx_context::sender(ctx),
    };
    transfer::share_object(config);
}

public fun update_shared_config(config: &mut SharedConfig, new_value: u64, ctx: &TxContext) {
    assert!(config.admin == tx_context::sender(ctx), 0);
    config.value = new_value;
}

public fun get_config_value(config: &SharedConfig): u64 {
    config.value
}

// ============ Immutable Objects ============

public struct ImmutableConfig has key {
    id: UID,
    name: vector<u8>,
    version: u64,
}

public fun create_immutable_config(
    name: vector<u8>,
    version: u64,
    ctx: &mut TxContext
) {
    let config = ImmutableConfig {
        id: object::new(ctx),
        name,
        version,
    };
    transfer::freeze_object(config);
}

// ============ Capability Pattern ============

public struct AdminCap has key, store {
    id: UID,
}

public struct Treasury has key {
    id: UID,
    balance: u64,
}

fun init(ctx: &mut TxContext) {
    let admin_cap = AdminCap { id: object::new(ctx) };
    transfer::transfer(admin_cap, tx_context::sender(ctx));

    let treasury = Treasury {
        id: object::new(ctx),
        balance: 0,
    };
    transfer::share_object(treasury);
}

public fun deposit(treasury: &mut Treasury, amount: u64) {
    treasury.balance = treasury.balance + amount;
}

public fun withdraw(
    _admin_cap: &AdminCap,
    treasury: &mut Treasury,
    amount: u64
): u64 {
    assert!(treasury.balance >= amount, 1);
    treasury.balance = treasury.balance - amount;
    amount
}

public fun transfer_admin(admin_cap: AdminCap, new_admin: address) {
    transfer::transfer(admin_cap, new_admin);
}

// ============ Public Transfer (with store) ============

public struct TransferableItem has key, store {
    id: UID,
    name: vector<u8>,
}

public fun create_transferable(name: vector<u8>, ctx: &mut TxContext): TransferableItem {
    TransferableItem {
        id: object::new(ctx),
        name,
    }
}

public fun send_item(item: TransferableItem, recipient: address) {
    transfer::public_transfer(item, recipient);
}
