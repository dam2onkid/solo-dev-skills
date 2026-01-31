# zkLogin

Zero-knowledge authentication using OAuth providers (Google, Apple, Facebook, Twitch).

## How It Works

1. User authenticates with OAuth provider → JWT token
2. Generate ephemeral keypair + nonce
3. Get ZK proof from prover service
4. Derive Sui address from JWT claims
5. Sign transactions with ephemeral key + ZK proof

## Installation

```bash
npm i @mysten/sui @mysten/zklogin
```

## Flow Implementation

```typescript
import { Ed25519Keypair } from "@mysten/sui/keypairs/ed25519";
import {
  generateNonce,
  generateRandomness,
  getExtendedEphemeralPublicKey,
  jwtToAddress,
  getZkLoginSignature,
} from "@mysten/sui/zklogin";

// 1. Generate ephemeral keypair (store securely, expires ~24h)
const ephemeralKeypair = new Ed25519Keypair();
const maxEpoch = currentEpoch + 2; // validity window

// 2. Generate randomness and nonce
const randomness = generateRandomness();
const nonce = generateNonce(
  ephemeralKeypair.getPublicKey(),
  maxEpoch,
  randomness
);

// 3. Redirect to OAuth provider with nonce
const authUrl = `https://accounts.google.com/o/oauth2/v2/auth?
  client_id=${CLIENT_ID}&
  redirect_uri=${REDIRECT_URI}&
  response_type=id_token&
  scope=openid&
  nonce=${nonce}`;

// 4. After OAuth callback, extract JWT
const jwt = extractJwtFromCallback();

// 5. Derive Sui address from JWT
const userSalt = getUserSalt(); // unique per user, store securely
const zkLoginAddress = jwtToAddress(jwt, userSalt);

// 6. Get ZK proof from prover
const extendedEphemeralPublicKey = getExtendedEphemeralPublicKey(
  ephemeralKeypair.getPublicKey()
);

const zkProof = await fetch("https://prover.mystenlabs.com/v1", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    jwt,
    extendedEphemeralPublicKey,
    maxEpoch,
    jwtRandomness: randomness,
    salt: userSalt,
    keyClaimName: "sub",
  }),
}).then((r) => r.json());
```

## Signing Transactions

```typescript
// Sign transaction with ephemeral key
const { bytes, signature: userSignature } = await tx.sign({
  client,
  signer: ephemeralKeypair,
});

// Combine with ZK proof
const zkLoginSignature = getZkLoginSignature({
  inputs: {
    ...zkProof,
    addressSeed: genAddressSeed(
      userSalt,
      "sub",
      decodedJwt.sub,
      decodedJwt.aud
    ).toString(),
  },
  maxEpoch,
  userSignature,
});

// Execute
await client.executeTransactionBlock({
  transactionBlock: bytes,
  signature: zkLoginSignature,
});
```

## Supported Providers

| Provider | iss claim                     |
| -------- | ----------------------------- |
| Google   | `https://accounts.google.com` |
| Apple    | `https://appleid.apple.com`   |
| Facebook | `https://www.facebook.com`    |
| Twitch   | `https://id.twitch.tv/oauth2` |
| Slack    | `https://slack.com`           |
| Kakao    | `https://kauth.kakao.com`     |

## Key Utilities

```typescript
import {
  generateNonce, // create nonce for OAuth
  generateRandomness, // random bytes for proof
  jwtToAddress, // JWT → Sui address
  getZkLoginSignature, // combine proof + signature
  hashASCIIStrToField, // hash for address seed
  poseidonHash, // Poseidon hash
} from "@mysten/sui/zklogin";
```

## Security Notes

- Ephemeral keypair expires after `maxEpoch`
- User salt must be stored securely (recovery impossible without it)
- JWT nonce binds OAuth session to ephemeral key
- ZK proof hides OAuth identity from blockchain
