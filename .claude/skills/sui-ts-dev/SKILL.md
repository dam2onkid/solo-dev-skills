---
name: sui-ts-dev
description: Build Sui blockchain apps with @mysten/sui TypeScript SDK. Use when creating SuiClient, building/signing transactions (PTB), querying objects/events/balances, using faucet, integrating React/Next.js dApp-kit hooks (useCurrentAccount, useSignTransaction, useConnectWallet, useSuiClientQuery), wallet connection, Move calls, zkLogin OAuth, Passkey WebAuthn, Walrus storage, Seal secrets, Nautilus TEE, SuiNS names, DeepBook DEX, Mysticeti consensus, or SUI tokenomics/staking.
---

# Sui TypeScript SDK

Build applications on the Sui blockchain using the official Mysten Labs TypeScript SDK.

## Quick Start

```bash
npm i @mysten/sui
npm i @mysten/dapp-kit  # for React apps
```

## Core Concepts

### SuiClient Setup

```typescript
import { getFullnodeUrl, SuiClient } from "@mysten/sui/client";

const client = new SuiClient({ url: getFullnodeUrl("devnet") });
```

### Transaction Building (PTB)

```typescript
import { Transaction } from "@mysten/sui/transactions";

const tx = new Transaction();
tx.moveCall({
  target: `${packageId}::module::function`,
  arguments: [tx.pure.string("arg1"), tx.object(objectId)],
});

const { bytes, signature } = await tx.sign({ client, signer: keypair });
const result = await client.executeTransactionBlock({
  transactionBlock: bytes,
  signature,
  options: { showEffects: true },
});
```

### React dApp-Kit

```typescript
import {
  ConnectButton,
  useCurrentAccount,
  useSignTransaction,
} from "@mysten/dapp-kit";

function App() {
  const account = useCurrentAccount();
  const { mutate: signTx } = useSignTransaction();
  return <ConnectButton />;
}
```

## References

### Core SDK

- [Client Setup](references/client-setup.md) - SuiClient, networks, faucet, keypairs
- [Transactions](references/transactions.md) - PTB, moveCall, signing, gas, sponsorship
- [Queries](references/queries.md) - Objects, coins, events, pagination
- [dApp Kit](references/dapp-kit.md) - React hooks, wallet, providers

### Framework Integration

- [React Integration](references/react-integration.md) - Providers, query hooks, transactions
- [Next.js Integration](references/nextjs-integration.md) - App Router, SSR, API routes
- [Best Practices](references/best-practices.md) - Error handling, caching, security

### Authentication

- [zkLogin](references/zklogin.md) - OAuth login (Google, Apple, Facebook)
- [Passkey](references/passkey.md) - WebAuthn biometric auth (Face ID, fingerprint)

### Infrastructure

- [Walrus](references/walrus.md) - Decentralized blob storage
- [Seal](references/seal.md) - Encrypted secrets with on-chain access control
- [Nautilus](references/nautilus.md) - TEE off-chain computation
- [SuiNS](references/suins.md) - Name service (alice.sui → 0x...)
- [DeepBook](references/deepbook.md) - Orderbook DEX, limit/market orders

### Protocol

- [Mysticeti](references/mysticeti.md) - DAG consensus protocol
- [Tokenomics](references/tokenomics.md) - SUI supply, staking, deflation

## External Resources

- [SDK Docs](https://sdk.mystenlabs.com/typescript)
- [dApp Kit](https://sdk.mystenlabs.com/dapp-kit)
- [TypeDoc API](https://sdk.mystenlabs.com/typedoc)
