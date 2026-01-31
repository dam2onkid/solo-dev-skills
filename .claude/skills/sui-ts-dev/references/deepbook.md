# DeepBook V3

High-performance decentralized orderbook exchange on Sui.

## Architecture

- **Pool**: Order book with Book (orders), State (user data), Vault (settlement)
- **BalanceManager**: Manages user funds for trading
- **DEEP Token**: Fee token with staking rewards

## TypeScript Integration

```typescript
import { Transaction } from "@mysten/sui/transactions";

const DEEPBOOK_PACKAGE = "0x..."; // DeepBook V3 package ID
const POOL_ID = "0x..."; // Trading pair pool

// Create balance manager
const tx = new Transaction();
tx.moveCall({
  target: `${DEEPBOOK_PACKAGE}::balance_manager::new`,
  arguments: [],
});
```

## Deposit to Balance Manager

```typescript
tx.moveCall({
  target: `${DEEPBOOK_PACKAGE}::balance_manager::deposit`,
  typeArguments: ["0x2::sui::SUI"],
  arguments: [tx.object(balanceManagerId), tx.object(coinId)],
});
```

## Place Limit Order (Move)

```move
use deepbook::pool::{Self, Pool};
use deepbook::balance_manager::{Self, BalanceManager};
use deepbook::constants;
use sui::clock::Clock;

public fun place_limit_buy<Base, Quote>(
    pool: &mut Pool<Base, Quote>,
    balance_manager: &mut BalanceManager,
    price: u64,      // quote per base (scaled 1e9)
    quantity: u64,   // base asset amount
    clock: &Clock,
    ctx: &TxContext,
) {
    let trade_proof = balance_manager::generate_proof_as_owner(
        balance_manager, ctx
    );

    pool::place_limit_order(
        pool,
        balance_manager,
        &trade_proof,
        0,                              // client_order_id
        constants::no_restriction(),    // GTC
        constants::cancel_taker(),      // self-matching
        price,
        quantity,
        true,                           // is_bid (buy)
        true,                           // pay_with_deep
        constants::max_u64(),           // never expire
        clock,
        ctx,
    );
}
```

## Place Market Order

```move
public fun market_buy<Base, Quote>(
    pool: &mut Pool<Base, Quote>,
    balance_manager: &mut BalanceManager,
    quantity: u64,
    clock: &Clock,
    ctx: &TxContext,
) {
    let trade_proof = balance_manager::generate_proof_as_owner(
        balance_manager, ctx
    );

    pool::place_market_order(
        pool,
        balance_manager,
        &trade_proof,
        0,
        constants::self_matching_allowed(),
        quantity,
        true,   // is_bid
        true,   // pay_with_deep
        clock,
        ctx,
    );
}
```

## Direct Swap (No BalanceManager)

```move
use sui::coin::Coin;
use token::deep::DEEP;

public fun swap_base_for_quote<Base, Quote>(
    pool: &mut Pool<Base, Quote>,
    base_in: Coin<Base>,
    deep_fee: Coin<DEEP>,
    min_quote_out: u64,
    clock: &Clock,
    ctx: &mut TxContext,
): (Coin<Base>, Coin<Quote>, Coin<DEEP>) {
    pool::swap_exact_base_for_quote(
        pool,
        base_in,
        deep_fee,
        min_quote_out,
        clock,
        ctx,
    )
}
```

## Cancel Orders

```move
// Single order
pool::cancel_order(pool, balance_manager, &trade_proof, order_id, clock, ctx);

// Multiple orders
pool::cancel_orders(pool, balance_manager, &trade_proof, order_ids, clock, ctx);

// All orders
pool::cancel_all_orders(pool, balance_manager, &trade_proof, clock, ctx);
```

## Order Types

| Constant                | Description                |
| ----------------------- | -------------------------- |
| `no_restriction()`      | Good-til-cancelled (GTC)   |
| `immediate_or_cancel()` | IOC - fill or cancel       |
| `fill_or_kill()`        | FOK - full fill or nothing |
| `post_only()`           | Maker only, no taker       |

## Self-Matching Options

| Option                    | Behavior              |
| ------------------------- | --------------------- |
| `self_matching_allowed()` | Allow self-trades     |
| `cancel_taker()`          | Cancel incoming order |
| `cancel_maker()`          | Cancel resting order  |

## Price Scaling

Prices are scaled by `1e9`:

- Price 1.5 = `1_500_000_000`
- Price 0.001 = `1_000_000`

## Flashloans

```move
let (base, quote, receipt) = pool::flashloan(pool, base_amount, quote_amount);
// Use funds...
pool::return_flashloan(pool, base, quote, receipt);
```
