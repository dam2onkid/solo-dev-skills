# Next.js Integration

## App Router Setup

### next.config.ts

```typescript
import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  serverExternalPackages: ["@mysten/walrus", "@mysten/walrus-wasm"],
  webpack: (config) => {
    config.externals.push("pino-pretty", "lokijs", "encoding");
    return config;
  },
};

export default nextConfig;
```

### Providers (Client Component)

```typescript
// src/app/providers.tsx
"use client";

import {
  createNetworkConfig,
  SuiClientProvider,
  WalletProvider,
} from "@mysten/dapp-kit";
import { getFullnodeUrl } from "@mysten/sui/client";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { useState } from "react";

const { networkConfig } = createNetworkConfig({
  mainnet: { url: getFullnodeUrl("mainnet") },
  testnet: { url: getFullnodeUrl("testnet") },
});

export function Providers({ children }: { children: React.ReactNode }) {
  const [queryClient] = useState(
    () =>
      new QueryClient({
        defaultOptions: {
          queries: {
            staleTime: 60_000,
            refetchOnWindowFocus: false,
          },
        },
      })
  );

  return (
    <QueryClientProvider client={queryClient}>
      <SuiClientProvider networks={networkConfig} defaultNetwork="mainnet">
        <WalletProvider autoConnect>{children}</WalletProvider>
      </SuiClientProvider>
    </QueryClientProvider>
  );
}
```

### Root Layout

```typescript
// src/app/layout.tsx
import { Providers } from "./providers";
import "@mysten/dapp-kit/dist/index.css"; // optional default styles

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}
```

## Server Components

### Server-side SuiClient

```typescript
// src/lib/sui-server.ts
import { SuiClient, getFullnodeUrl } from "@mysten/sui/client";

export const suiClient = new SuiClient({
  url: getFullnodeUrl("mainnet"),
});

// Usage in Server Component
// src/app/object/[id]/page.tsx
import { suiClient } from "@/lib/sui-server";

export default async function ObjectPage({
  params,
}: {
  params: { id: string };
}) {
  const object = await suiClient.getObject({
    id: params.id,
    options: { showContent: true },
  });

  return <pre>{JSON.stringify(object, null, 2)}</pre>;
}
```

### API Routes

```typescript
// src/app/api/balance/[address]/route.ts
import { suiClient } from "@/lib/sui-server";
import { NextResponse } from "next/server";

export async function GET(
  request: Request,
  { params }: { params: { address: string } }
) {
  try {
    const balance = await suiClient.getBalance({
      owner: params.address,
    });
    return NextResponse.json(balance);
  } catch (error) {
    return NextResponse.json(
      { error: "Failed to fetch balance" },
      { status: 500 }
    );
  }
}
```

## Hydration Safety

### Client-only Components

```typescript
// src/components/wallet-button.tsx
"use client";

import { ConnectButton } from "@mysten/dapp-kit";
import dynamic from "next/dynamic";

function WalletButton() {
  return <ConnectButton />;
}

// Prevent SSR hydration mismatch
export default dynamic(() => Promise.resolve(WalletButton), {
  ssr: false,
});
```

### Mounted Check

```typescript
"use client";

import { useCurrentAccount } from "@mysten/dapp-kit";
import { useEffect, useState } from "react";

export function WalletStatus() {
  const account = useCurrentAccount();
  const [mounted, setMounted] = useState(false);

  useEffect(() => setMounted(true), []);

  if (!mounted) return <div>Loading...</div>;

  return account ? (
    <span>{account.address.slice(0, 8)}...</span>
  ) : (
    <span>Not connected</span>
  );
}
```

## Pages Router (Legacy)

### \_app.tsx

```typescript
// pages/_app.tsx
import {
  createNetworkConfig,
  SuiClientProvider,
  WalletProvider,
} from "@mysten/dapp-kit";
import { getFullnodeUrl } from "@mysten/sui/client";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import type { AppProps } from "next/app";

const { networkConfig } = createNetworkConfig({
  mainnet: { url: getFullnodeUrl("mainnet") },
});

const queryClient = new QueryClient();

export default function App({ Component, pageProps }: AppProps) {
  return (
    <QueryClientProvider client={queryClient}>
      <SuiClientProvider networks={networkConfig} defaultNetwork="mainnet">
        <WalletProvider>
          <Component {...pageProps} />
        </WalletProvider>
      </SuiClientProvider>
    </QueryClientProvider>
  );
}
```

### getServerSideProps

```typescript
// pages/object/[id].tsx
import { SuiClient, getFullnodeUrl } from "@mysten/sui/client";
import type { GetServerSideProps } from "next";

export const getServerSideProps: GetServerSideProps = async ({ params }) => {
  const client = new SuiClient({ url: getFullnodeUrl("mainnet") });
  const object = await client.getObject({
    id: params?.id as string,
    options: { showContent: true },
  });

  return { props: { object } };
};
```

## Environment Variables

```env
# .env.local
NEXT_PUBLIC_SUI_NETWORK=mainnet
NEXT_PUBLIC_PACKAGE_ID=0x...

# Server-only (no NEXT_PUBLIC_ prefix)
SUI_ADMIN_KEY=...
```

```typescript
// Usage
const network = process.env.NEXT_PUBLIC_SUI_NETWORK as "mainnet" | "testnet";
```
