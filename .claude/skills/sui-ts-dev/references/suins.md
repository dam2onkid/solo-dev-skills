# SuiNS

Sui Name Service - human-readable names for Sui addresses.

## TypeScript SDK

```bash
npm i @mysten/suins
```

```typescript
import { SuinsClient } from "@mysten/suins";
import { SuiClient, getFullnodeUrl } from "@mysten/sui/client";

const suiClient = new SuiClient({ url: getFullnodeUrl("mainnet") });
const suinsClient = new SuinsClient({ client: suiClient });
```

## Resolve Name → Address

```typescript
// SDK method
const nameRecord = await suinsClient.getNameRecord("demo.sui");
const address = nameRecord?.targetAddress;

// Or via SuiClient RPC
const address = await suiClient.resolveNameServiceAddress({
  name: "demo.sui",
});
```

## Resolve Address → Name

```typescript
const names = await suiClient.resolveNameServiceNames({
  address: "0x...",
});
// Returns array of names pointing to this address
```

## Query Name Record

```typescript
const record = await suinsClient.getNameRecord("demo.sui");

console.log({
  name: record.name,
  targetAddress: record.targetAddress,
  expirationTimestampMs: record.expirationTimestampMs,
  avatar: record.avatar,
  contentHash: record.contentHash,
});
```

## Move Integration

```move
module myapp::transfer;

use suins::suins::SuiNS;
use suins::registry::Registry;
use suins::domain;
use sui::clock::Clock;

const ENameNotFound: u64 = 0;
const ENameExpired: u64 = 1;
const ENoTargetAddress: u64 = 2;

public fun send_to_name<T: key + store>(
    suins: &SuiNS,
    obj: T,
    name: String,
    clock: &Clock,
) {
    let registry = suins.registry<Registry>();
    let domain = domain::new(name);

    let mut optional = registry.lookup(domain);
    assert!(optional.is_some(), ENameNotFound);

    let record = optional.extract();
    assert!(!record.has_expired(clock), ENameExpired);
    assert!(record.target_address().is_some(), ENoTargetAddress);

    transfer::public_transfer(obj, record.target_address().extract());
}
```

## Subdomains

```typescript
// Get all subdomains for a parent
const subdomains = await suinsClient.getSubnames("example.sui");
// Returns: ['sub1.example.sui', 'sub2.example.sui', ...]
```

## API Endpoints

| Method   | Endpoint                            |
| -------- | ----------------------------------- |
| JSON-RPC | `suix_resolveNameServiceAddress`    |
| GraphQL  | `resolveSuinsAddress` query         |
| GraphQL  | `defaultSuinsName` field on Address |

## Name Format

- Minimum 3 characters
- Lowercase letters, numbers, hyphens
- Ends with `.sui`
- Subdomains: `sub.name.sui`

## Registration

Names are registered through the SuiNS dApp or contracts. Registration requires:

- Payment in SUI
- Duration (1-5 years)
- Unique name availability

## Use Cases

- Wallet addresses: `alice.sui` instead of `0x123...`
- Transfer to names: Send tokens to `bob.sui`
- dApp profiles: Link avatar, website, social handles
- Subdomains: `app.company.sui` for projects
