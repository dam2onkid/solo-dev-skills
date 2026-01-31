# Seal

Decentralized secrets management with on-chain access control policies.

## Overview

Seal encrypts data client-side, stores encrypted blobs on Walrus/IPFS, and uses Sui Move contracts to define who can decrypt. Key servers only release decryption keys when access policy passes.

## Installation

```bash
npm i @aspect-build/seal-sdk
```

## Encrypt Data

```typescript
import { SealClient } from '@aspect-build/seal-sdk';

const client = new SealClient({ network: 'testnet' });

const { encryptedObject, key: backupKey } = await client.encrypt({
  threshold: 2,           // min key servers needed
  packageId: '0x...',     // Move package with access policy
  id: '0x...',            // unique encryption ID
  data: new Uint8Array([...]),
});

// Store encryptedObject on Walrus/IPFS
```

## Decrypt Data

```typescript
import { Transaction } from "@mysten/sui/transactions";

// Build transaction that calls seal_approve
const tx = new Transaction();
tx.moveCall({
  target: `${packageId}::${module}::seal_approve`,
  arguments: [
    tx.pure.vector("u8", id),
    // other arguments required by policy
  ],
});

const txBytes = await tx.build({
  client: suiClient,
  onlyTransactionKind: true,
});

// Decrypt with session key
const decryptedBytes = await client.decrypt({
  data: encryptedBytes,
  sessionKey,
  txBytes,
});
```

## Move Access Control

```move
module myapp::access;

use sui::clock::Clock;

const ENoAccess: u64 = 1;

// Time-lock: decrypt only after timestamp
entry fun seal_approve(id: vector<u8>, clock: &Clock) {
    let mut bcs = sui::bcs::new(id);
    let unlock_time = bcs.peel_u64();
    assert!(clock.timestamp_ms() >= unlock_time, ENoAccess);
}
```

## Access Control Patterns

### NFT Ownership

```move
entry fun seal_approve(id: vector<u8>, nft: &MyNFT, ctx: &TxContext) {
    assert!(nft.owner() == ctx.sender(), ENoAccess);
}
```

### Token Gating

```move
entry fun seal_approve(id: vector<u8>, coin: &Coin<SUI>) {
    assert!(coin.value() >= 1_000_000_000, ENoAccess); // 1 SUI min
}
```

### Allowlist

```move
entry fun seal_approve(id: vector<u8>, allowlist: &Allowlist, ctx: &TxContext) {
    assert!(allowlist.contains(ctx.sender()), ENoAccess);
}
```

### Multi-condition

```move
entry fun seal_approve(
    id: vector<u8>,
    nft: &MyNFT,
    clock: &Clock,
    ctx: &TxContext
) {
    assert!(nft.owner() == ctx.sender(), ENoAccess);
    assert!(clock.timestamp_ms() >= nft.unlock_time(), ENoAccess);
}
```

## Key Concepts

| Term           | Description                            |
| -------------- | -------------------------------------- |
| `threshold`    | Min key servers needed to decrypt      |
| `packageId`    | Move package containing `seal_approve` |
| `id`           | Unique identifier for encrypted object |
| `sessionKey`   | Temporary key for decryption session   |
| `seal_approve` | Entry function defining access policy  |

## Security Model

- Client-side encryption (data never exposed to servers)
- Threshold cryptography (no single point of failure)
- On-chain access control (transparent, auditable)
- `seal_approve` must be side-effect free (read-only)

## Use Cases

- Private NFT content
- Subscription-gated content
- Time-locked reveals
- DAO-controlled secrets
- Encrypted messaging
