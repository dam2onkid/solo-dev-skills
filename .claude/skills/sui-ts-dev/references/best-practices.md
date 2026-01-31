# Best Practices

## Project Setup

### Scaffold with create-dapp

```bash
npm create @mysten/dapp
# Templates:
# - react-client-dapp: Basic wallet + object fetching
# - react-e2e-counter: Full stack with Move contract
```

### Production RPC

```typescript
// DON'T use public endpoints in production (rate limited: 100 req/30s)
const client = new SuiClient({ url: getFullnodeUrl("mainnet") }); // ❌

// DO use dedicated RPC providers
const client = new SuiClient({
  url: process.env.NEXT_PUBLIC_RPC_URL, // ✅
});
```

## Error Handling

### Transaction Errors

```typescript
import { useSignAndExecuteTransaction } from "@mysten/dapp-kit";

const { mutate, error, reset } = useSignAndExecuteTransaction();

mutate(
  { transaction: tx },
  {
    onError: (error) => {
      if (error.message.includes("Insufficient gas")) {
        showToast("Not enough SUI for gas");
      } else if (error.message.includes("rejected")) {
        showToast("Transaction rejected by user");
      } else {
        showToast("Transaction failed");
        console.error(error);
      }
    },
  }
);
```

### Query Error Boundaries

```typescript
import { QueryErrorResetBoundary } from "@tanstack/react-query";
import { ErrorBoundary } from "react-error-boundary";

function App() {
  return (
    <QueryErrorResetBoundary>
      {({ reset }) => (
        <ErrorBoundary
          onReset={reset}
          fallbackRender={({ resetErrorBoundary }) => (
            <div>
              <p>Something went wrong</p>
              <button onClick={resetErrorBoundary}>Try again</button>
            </div>
          )}
        >
          <YourApp />
        </ErrorBoundary>
      )}
    </QueryErrorResetBoundary>
  );
}
```

### Retry Logic

```typescript
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: (failureCount, error) => {
        // Don't retry on 4xx errors
        if (error.message.includes("not found")) return false;
        return failureCount < 3;
      },
      retryDelay: (attemptIndex) => Math.min(1000 * 2 ** attemptIndex, 30000),
    },
  },
});
```

## Performance

### Query Caching

```typescript
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 60_000, // Data fresh for 1 min
      gcTime: 10 * 60_000, // Cache for 10 min
      refetchOnWindowFocus: false, // Disable auto-refetch
      refetchOnReconnect: true,
    },
  },
});
```

### Selective Data Fetching

```typescript
// Only fetch what you need
const { data } = useSuiClientQuery("getObject", {
  id: objectId,
  options: {
    showContent: true, // ✅ Need content
    showOwner: false, // ❌ Don't need
    showPreviousTransaction: false,
    showStorageRebate: false,
  },
});
```

### Batch Queries

```typescript
// Instead of multiple single queries
const obj1 = useSuiClientQuery("getObject", { id: id1 }); // ❌
const obj2 = useSuiClientQuery("getObject", { id: id2 }); // ❌

// Use multiGetObjects
const { data } = useSuiClientQuery("multiGetObjects", {
  ids: [id1, id2, id3],
  options: { showContent: true },
}); // ✅
```

### Prefetching

```typescript
import { useQueryClient } from "@tanstack/react-query";
import { useSuiClient } from "@mysten/dapp-kit";

function ObjectList({ ids }: { ids: string[] }) {
  const queryClient = useQueryClient();
  const client = useSuiClient();

  // Prefetch on hover
  const prefetch = (id: string) => {
    queryClient.prefetchQuery({
      queryKey: ["getObject", { id }],
      queryFn: () => client.getObject({ id, options: { showContent: true } }),
    });
  };

  return ids.map((id) => (
    <Link key={id} href={`/object/${id}`} onMouseEnter={() => prefetch(id)}>
      {id}
    </Link>
  ));
}
```

## Transaction Building

### Gas Estimation

```typescript
const tx = new Transaction();
tx.moveCall({ target, arguments });

// Dry run first
const dryRun = await client.dryRunTransactionBlock({
  transactionBlock: await tx.build({ client }),
});

if (dryRun.effects.status.status === "failure") {
  throw new Error(dryRun.effects.status.error);
}

// Set gas budget with buffer
const gasUsed =
  BigInt(dryRun.effects.gasUsed.computationCost) +
  BigInt(dryRun.effects.gasUsed.storageCost);
tx.setGasBudget((gasUsed * 120n) / 100n); // 20% buffer
```

### Object Freshness

```typescript
// Always get fresh object data before transactions
const { data: coin } = await client.getObject({
  id: coinId,
  options: { showContent: true },
});

// Use the fresh version
tx.object(coin.data.objectId); // Has latest version/digest
```

## Security

### Input Validation

```typescript
// Validate addresses
import { isValidSuiAddress } from "@mysten/sui/utils";

function SendForm() {
  const [recipient, setRecipient] = useState("");

  const isValid = isValidSuiAddress(recipient);

  return (
    <input
      value={recipient}
      onChange={(e) => setRecipient(e.target.value)}
      className={isValid ? "valid" : "invalid"}
    />
  );
}
```

### Environment Secrets

```typescript
// Never expose private keys in client code
// ❌ BAD
const keypair = Ed25519Keypair.fromSecretKey(process.env.NEXT_PUBLIC_KEY);

// ✅ GOOD - Server-side only
// src/app/api/sign/route.ts
const keypair = Ed25519Keypair.fromSecretKey(process.env.ADMIN_KEY);
```

## Type Safety

### Typed Move Calls

```typescript
// Define types for your contract
interface MyObject {
  id: string;
  name: string;
  value: bigint;
}

function parseMyObject(data: SuiParsedData): MyObject | null {
  if (data.dataType !== "moveObject") return null;
  const fields = data.fields as Record<string, unknown>;
  return {
    id: fields.id as string,
    name: fields.name as string,
    value: BigInt(fields.value as string),
  };
}
```

### Generic Query Wrapper

```typescript
function useMyObjects(owner: string) {
  return useSuiClientQuery(
    "getOwnedObjects",
    {
      owner,
      filter: { StructType: `${PACKAGE_ID}::module::MyObject` },
      options: { showContent: true },
    },
    {
      select: (data) =>
        data.data
          .map((obj) => obj.data?.content)
          .filter(Boolean)
          .map(parseMyObject)
          .filter(Boolean),
    }
  );
}
```
