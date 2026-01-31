# Queries

## Object Queries

```typescript
// Single object
const obj = await client.getObject({
  id: objectId,
  options: { showContent: true, showOwner: true },
});

// Multiple objects
const objs = await client.multiGetObjects({
  ids: [id1, id2],
  options: { showContent: true },
});

// Owned objects
const owned = await client.getOwnedObjects({
  owner: address,
  filter: { StructType: `${packageId}::module::Type` },
  options: { showContent: true },
});

// Dynamic fields
const fields = await client.getDynamicFields({ parentId: objectId });
const field = await client.getDynamicFieldObject({
  parentId: objectId,
  name: { type: "u64", value: "1" },
});
```

## Coin Queries

```typescript
// Balance
const balance = await client.getBalance({
  owner: address,
  coinType: "0x2::sui::SUI", // optional, defaults to SUI
});

// All balances
const allBalances = await client.getAllBalances({ owner: address });

// Coins
const coins = await client.getCoins({
  owner: address,
  coinType: "0x2::sui::SUI",
});

// All coins
const allCoins = await client.getAllCoins({ owner: address });

// Total supply
const supply = await client.getTotalSupply({ coinType });
```

## Event Queries

```typescript
// Query events
const events = await client.queryEvents({
  query: { MoveEventType: `${packageId}::module::EventType` },
  limit: 50,
});

// By sender
const bySender = await client.queryEvents({
  query: { Sender: address },
});

// By transaction
const byTx = await client.queryEvents({
  query: { Transaction: txDigest },
});

// Subscribe (websocket)
const unsubscribe = await client.subscribeEvent({
  filter: { MoveEventType: eventType },
  onMessage: (event) => console.log(event),
});
```

## Transaction Queries

```typescript
// Single transaction
const tx = await client.getTransactionBlock({
  digest: txDigest,
  options: { showEffects: true, showInput: true },
});

// Query transactions
const txs = await client.queryTransactionBlocks({
  filter: { FromAddress: address },
  options: { showEffects: true },
  limit: 10,
});
```

## Pagination

```typescript
let cursor = null;
const allObjects = [];

do {
  const page = await client.getOwnedObjects({
    owner: address,
    cursor,
    limit: 50,
  });
  allObjects.push(...page.data);
  cursor = page.hasNextPage ? page.nextCursor : null;
} while (cursor);
```

## Move Call Dry Run

```typescript
const tx = new Transaction();
tx.moveCall({ target, arguments });

const dryRun = await client.dryRunTransactionBlock({
  transactionBlock: await tx.build({ client }),
});
// Check dryRun.effects before executing
```
