# Walrus

Decentralized blob storage protocol for large binary files on Sui.

## Installation

```bash
npm i @mysten/sui
```

## Setup

```typescript
import { getFullnodeUrl, SuiClient } from "@mysten/sui/client";
import { walrus } from "@mysten/sui/walrus";

// Direct storage node access
const client = new SuiClient({
  url: getFullnodeUrl("testnet"),
}).$extend(walrus());

// Or with upload relay (recommended for browsers)
const clientWithRelay = new SuiClient({
  url: getFullnodeUrl("testnet"),
}).$extend(
  walrus({
    uploadRelay: {
      host: "https://upload-relay.testnet.walrus.space",
      sendTip: { max: 1_000 }, // optional tip
    },
  })
);
```

## Write Blob

```typescript
import { Ed25519Keypair } from "@mysten/sui/keypairs/ed25519";

const keypair = new Ed25519Keypair();
const data = new TextEncoder().encode("Hello Walrus!");

const { blobId } = await client.walrus.writeBlob({
  blob: data,
  deletable: false, // immutable
  epochs: 3, // storage duration
  signer: keypair,
});

console.log("Blob ID:", blobId);
```

## Read Blob

```typescript
const blob = await client.walrus.readBlob({ blobId });
const text = new TextDecoder().decode(blob);
```

## WalrusFile API

```typescript
import { WalrusFile } from "@mysten/sui/walrus";

// From various sources
const file1 = WalrusFile.from({
  contents: new Uint8Array([1, 2, 3]),
  identifier: "data.bin",
});

const file2 = WalrusFile.from({
  contents: new Blob([data]),
  identifier: "image.png",
});

const file3 = WalrusFile.from({
  contents: new TextEncoder().encode("# README"),
  identifier: "README.md",
  tags: { "content-type": "text/markdown" },
});

// Write multiple files
const results = await client.walrus.writeFiles({
  files: [file1, file2, file3],
  epochs: 3,
  deletable: true,
  signer: keypair,
});

// Results contain { id, blobId, blobObject }
```

## Read Files

```typescript
// Read single file
const file = await client.walrus.readFile({ id: fileId });

// Read multiple
const files = await client.walrus.readFiles({ ids: [id1, id2] });
```

## Storage Parameters

| Parameter   | Description                               |
| ----------- | ----------------------------------------- |
| `epochs`    | Number of epochs to store (1 epoch ≈ 24h) |
| `deletable` | If `true`, owner can delete before expiry |
| `signer`    | Keypair to pay storage fees               |

## Networks

| Network | Upload Relay                                |
| ------- | ------------------------------------------- |
| Testnet | `https://upload-relay.testnet.walrus.space` |
| Mainnet | `https://upload-relay.walrus.space`         |

## Use Cases

- NFT media storage
- dApp static assets
- User-generated content
- Backup/archival
- Large dataset storage

## Aggregator URLs

Direct blob access via HTTP:

```
https://aggregator.walrus.space/v1/blobs/{blobId}
```
