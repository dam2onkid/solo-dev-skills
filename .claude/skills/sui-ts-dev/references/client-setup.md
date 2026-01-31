# SuiClient Setup & Configuration

## Installation

```bash
npm i @mysten/sui
```

## Client Initialization

```typescript
import { getFullnodeUrl, SuiClient } from "@mysten/sui/client";

// Devnet (testing, faucet available)
const devnet = new SuiClient({ url: getFullnodeUrl("devnet") });

// Testnet (staging)
const testnet = new SuiClient({ url: getFullnodeUrl("testnet") });

// Mainnet (production)
const mainnet = new SuiClient({ url: getFullnodeUrl("mainnet") });

// Custom RPC
const custom = new SuiClient({ url: "https://your-rpc.example.com" });
```

## Faucet (Devnet/Testnet only)

```typescript
import { getFaucetHost, requestSuiFromFaucetV2 } from "@mysten/sui/faucet";

await requestSuiFromFaucetV2({
  host: getFaucetHost("devnet"),
  recipient: "0xYourAddress...",
});
```

## Balance Query

```typescript
import { MIST_PER_SUI } from "@mysten/sui/utils";

const balance = await client.getBalance({ owner: address });
const sui = Number(balance.totalBalance) / Number(MIST_PER_SUI);
```

## Keypair Generation

```typescript
import { Ed25519Keypair } from "@mysten/sui/keypairs/ed25519";

// Generate new
const keypair = new Ed25519Keypair();
console.log(keypair.getPublicKey().toSuiAddress());

// From secret key
const fromSecret = Ed25519Keypair.fromSecretKey(secretKeyBytes);

// From mnemonic
import { derivePath } from "@mysten/sui/crypto";
const fromMnemonic = Ed25519Keypair.deriveKeypair(mnemonic);
```

## Network Config (React)

```typescript
import { createNetworkConfig } from "@mysten/dapp-kit";

const { networkConfig } = createNetworkConfig({
  devnet: { url: getFullnodeUrl("devnet") },
  testnet: { url: getFullnodeUrl("testnet") },
  mainnet: { url: getFullnodeUrl("mainnet") },
});
```
