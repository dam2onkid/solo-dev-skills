# dApp Kit (React)

React hooks and components for Sui wallet integration.

## Installation

```bash
npm i @mysten/dapp-kit @tanstack/react-query
```

## Provider Setup

```typescript
import { SuiClientProvider, WalletProvider } from "@mysten/dapp-kit";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { getFullnodeUrl } from "@mysten/sui/client";

const queryClient = new QueryClient();
const networks = {
  devnet: { url: getFullnodeUrl("devnet") },
  mainnet: { url: getFullnodeUrl("mainnet") },
};

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <SuiClientProvider networks={networks} defaultNetwork="devnet">
        <WalletProvider>
          <YourApp />
        </WalletProvider>
      </SuiClientProvider>
    </QueryClientProvider>
  );
}
```

## Wallet Connection

```typescript
import { ConnectButton, useCurrentAccount } from "@mysten/dapp-kit";

function WalletStatus() {
  const account = useCurrentAccount();

  return (
    <div>
      <ConnectButton />
      {account && <p>Connected: {account.address}</p>}
    </div>
  );
}
```

## Wallet Hooks

```typescript
import {
  useCurrentAccount, // current connected account
  useCurrentWallet, // current wallet instance
  useAccounts, // all accounts in wallet
  useWallets, // all available wallets
  useConnectWallet, // connect to wallet
  useDisconnectWallet, // disconnect wallet
  useSwitchAccount, // switch between accounts
} from "@mysten/dapp-kit";

// Connect programmatically
const { mutate: connect } = useConnectWallet();
connect({ wallet: selectedWallet });

// Disconnect
const { mutate: disconnect } = useDisconnectWallet();
disconnect();
```

## Transaction Signing

```typescript
import {
  useSignTransaction,
  useSignAndExecuteTransaction,
} from "@mysten/dapp-kit";
import { Transaction } from "@mysten/sui/transactions";

function SendTx() {
  const { mutate: signAndExecute } = useSignAndExecuteTransaction();

  const handleClick = () => {
    const tx = new Transaction();
    tx.moveCall({ target: "...", arguments: [] });

    signAndExecute(
      { transaction: tx },
      {
        onSuccess: (result) => console.log("Success:", result.digest),
        onError: (error) => console.error("Error:", error),
      }
    );
  };

  return <button onClick={handleClick}>Send</button>;
}
```

## Message Signing

```typescript
import { useSignPersonalMessage } from "@mysten/dapp-kit";

const { mutate: signMessage } = useSignPersonalMessage();

signMessage(
  { message: new TextEncoder().encode("Hello Sui!") },
  { onSuccess: ({ signature }) => console.log(signature) }
);
```

## Query Hooks

```typescript
import { useSuiClientQuery, useSuiClientInfiniteQuery } from "@mysten/dapp-kit";

// Single query
const { data, isLoading } = useSuiClientQuery("getBalance", {
  owner: address,
});

// Infinite scroll
const { data, fetchNextPage, hasNextPage } = useSuiClientInfiniteQuery(
  "getOwnedObjects",
  { owner: address },
  {
    select: (data) => data.pages.flatMap((page) => page.data),
  }
);
```

## SuiClient Access

```typescript
import { useSuiClient } from "@mysten/dapp-kit";

function Component() {
  const client = useSuiClient();
  // Use client for direct API calls
}
```

## Network Switching

```typescript
import { useSuiClientContext } from "@mysten/dapp-kit";

function NetworkSwitcher() {
  const ctx = useSuiClientContext();

  return (
    <select
      value={ctx.network}
      onChange={(e) => ctx.selectNetwork(e.target.value)}
    >
      <option value="devnet">Devnet</option>
      <option value="mainnet">Mainnet</option>
    </select>
  );
}
```
