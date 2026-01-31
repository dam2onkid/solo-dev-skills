# React Integration

## Installation

```bash
npm i @mysten/sui @mysten/dapp-kit @tanstack/react-query
```

## Provider Setup

```typescript
// src/providers.tsx
import {
  createNetworkConfig,
  SuiClientProvider,
  WalletProvider,
} from "@mysten/dapp-kit";
import { getFullnodeUrl } from "@mysten/sui/client";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";

const { networkConfig } = createNetworkConfig({
  devnet: { url: getFullnodeUrl("devnet") },
  testnet: { url: getFullnodeUrl("testnet") },
  mainnet: { url: getFullnodeUrl("mainnet") },
});

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 60_000, // 1 minute
      gcTime: 10 * 60_000, // 10 minutes (formerly cacheTime)
      retry: 3,
      refetchOnWindowFocus: false,
    },
  },
});

export function Providers({ children }: { children: React.ReactNode }) {
  return (
    <QueryClientProvider client={queryClient}>
      <SuiClientProvider networks={networkConfig} defaultNetwork="mainnet">
        <WalletProvider autoConnect>{children}</WalletProvider>
      </SuiClientProvider>
    </QueryClientProvider>
  );
}
```

## Query Hooks

### Single Query

```typescript
import { useSuiClientQuery } from "@mysten/dapp-kit";

function Balance({ address }: { address: string }) {
  const { data, isPending, error } = useSuiClientQuery("getBalance", {
    owner: address,
  });

  if (isPending) return <div>Loading...</div>;
  if (error) return <div>Error: {error.message}</div>;

  return <div>Balance: {data.totalBalance}</div>;
}
```

### Multiple Queries

```typescript
import { useSuiClientQueries } from "@mysten/dapp-kit";

function Dashboard({ address }: { address: string }) {
  const { data, isPending, isError } = useSuiClientQueries({
    queries: [
      { method: "getAllBalances", params: { owner: address } },
      { method: "getOwnedObjects", params: { owner: address } },
    ],
    combine: (results) => ({
      data: results.map((r) => r.data),
      isPending: results.some((r) => r.isPending),
      isError: results.some((r) => r.isError),
    }),
  });

  if (isPending) return <div>Loading...</div>;
  return <pre>{JSON.stringify(data, null, 2)}</pre>;
}
```

### Infinite Query (Pagination)

```typescript
import { useSuiClientInfiniteQuery } from "@mysten/dapp-kit";

function ObjectList({ address }: { address: string }) {
  const { data, fetchNextPage, hasNextPage, isFetchingNextPage } =
    useSuiClientInfiniteQuery("getOwnedObjects", {
      owner: address,
    });

  const objects = data?.pages.flatMap((page) => page.data) ?? [];

  return (
    <div>
      {objects.map((obj) => (
        <div key={obj.data?.objectId}>{obj.data?.objectId}</div>
      ))}
      {hasNextPage && (
        <button onClick={() => fetchNextPage()} disabled={isFetchingNextPage}>
          {isFetchingNextPage ? "Loading..." : "Load More"}
        </button>
      )}
    </div>
  );
}
```

## Transaction Hooks

### Sign and Execute

```typescript
import {
  useSignAndExecuteTransaction,
  useCurrentAccount,
} from "@mysten/dapp-kit";
import { Transaction } from "@mysten/sui/transactions";

function SendButton() {
  const account = useCurrentAccount();
  const { mutate: signAndExecute, isPending } = useSignAndExecuteTransaction();

  const handleSend = () => {
    const tx = new Transaction();
    tx.moveCall({
      target: `${PACKAGE_ID}::module::function`,
      arguments: [],
    });

    signAndExecute(
      { transaction: tx },
      {
        onSuccess: (result) => {
          console.log("Digest:", result.digest);
        },
        onError: (error) => {
          console.error("Failed:", error);
        },
      }
    );
  };

  return (
    <button onClick={handleSend} disabled={!account || isPending}>
      {isPending ? "Sending..." : "Send"}
    </button>
  );
}
```

### Sign Only (for sponsored tx)

```typescript
import { useSignTransaction } from "@mysten/dapp-kit";

const { mutate: signTx } = useSignTransaction();

signTx(
  { transaction: tx },
  {
    onSuccess: ({ bytes, signature }) => {
      // Send to sponsor for execution
    },
  }
);
```

## Wallet Components

```typescript
import {
  ConnectButton,
  ConnectModal,
  useCurrentAccount,
} from "@mysten/dapp-kit";

function Header() {
  const account = useCurrentAccount();

  return (
    <header>
      <ConnectButton />
      {account && <span>Connected: {account.address}</span>}
    </header>
  );
}

// Custom modal trigger
function CustomConnect() {
  const [open, setOpen] = useState(false);

  return (
    <>
      <button onClick={() => setOpen(true)}>Connect Wallet</button>
      <ConnectModal open={open} onOpenChange={setOpen} />
    </>
  );
}
```

## Network Switching

```typescript
import { useSuiClientContext } from "@mysten/dapp-kit";

function NetworkSelector() {
  const { network, selectNetwork } = useSuiClientContext();

  return (
    <select value={network} onChange={(e) => selectNetwork(e.target.value)}>
      <option value="mainnet">Mainnet</option>
      <option value="testnet">Testnet</option>
      <option value="devnet">Devnet</option>
    </select>
  );
}
```

## Direct Client Access

```typescript
import { useSuiClient } from "@mysten/dapp-kit";

function CustomQuery() {
  const client = useSuiClient();

  useEffect(() => {
    client
      .getObject({ id: objectId, options: { showContent: true } })
      .then(setObject);
  }, [client, objectId]);
}
```
