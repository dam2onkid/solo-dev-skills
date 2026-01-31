# Transactions (PTB)

Programmable Transaction Blocks (PTB) compose multiple operations in a single atomic transaction.

## Basic Transaction

```typescript
import { Transaction } from "@mysten/sui/transactions";

const tx = new Transaction();
```

## Move Call

```typescript
tx.moveCall({
  target: `${packageId}::module::function_name`,
  arguments: [
    tx.pure.string("string_arg"),
    tx.pure.u64(12345n),
    tx.pure.bool(true),
    tx.pure.address("0x..."),
    tx.object(objectId), // existing object
    tx.pure.vector("u8", [1, 2, 3]), // vector
  ],
  typeArguments: ["0x2::coin::Coin<0x2::sui::SUI>"], // generics
});
```

## Common Operations

```typescript
// Transfer SUI
tx.transferObjects([tx.gas], recipient);

// Split coins
const [coin] = tx.splitCoins(tx.gas, [tx.pure.u64(1000000000n)]);
tx.transferObjects([coin], recipient);

// Merge coins
tx.mergeCoins(destinationCoin, [coin1, coin2]);

// Publish package
tx.publish({ modules, dependencies });

// Make Move Vec
const vec = tx.makeMoveVec({ elements: [obj1, obj2] });
```

## Sign & Execute

```typescript
// Method 1: Separate sign + execute
const { bytes, signature } = await tx.sign({ client, signer: keypair });
const result = await client.executeTransactionBlock({
  transactionBlock: bytes,
  signature,
  requestType: "WaitForLocalExecution",
  options: { showEffects: true, showObjectChanges: true },
});

// Method 2: signAndExecuteTransaction
const result = await client.signAndExecuteTransaction({
  signer: keypair,
  transaction: tx,
  options: { showEffects: true },
});
```

## Transaction Options

```typescript
options: {
  showInput: true,           // show transaction input
  showEffects: true,         // show execution effects
  showEvents: true,          // show emitted events
  showObjectChanges: true,   // show object mutations
  showBalanceChanges: true,  // show balance changes
  showRawEffects: true,      // raw BCS effects
}
```

## Gas Configuration

```typescript
tx.setGasBudget(10000000n);
tx.setGasPrice(1000n);
tx.setGasOwner(sponsorAddress);
tx.setGasPayment([{ objectId, version, digest }]);
```

## Sponsored Transactions

```typescript
// Sponsor sets gas
tx.setGasOwner(sponsorAddress);
tx.setGasPayment(sponsorCoins);

// Sender builds
const txBytes = await tx.build({ client });

// Sponsor signs
const sponsorSig = await sponsorKeypair.signTransaction(txBytes);

// Sender signs
const senderSig = await senderKeypair.signTransaction(txBytes);

// Execute with both signatures
await client.executeTransactionBlock({
  transactionBlock: txBytes,
  signature: [senderSig.signature, sponsorSig.signature],
});
```
