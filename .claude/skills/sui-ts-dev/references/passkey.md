# Passkey Authentication

WebAuthn/FIDO2 biometric authentication (fingerprint, Face ID) for Sui wallets.

## Installation

```bash
npm i @mysten/sui
```

## Create Passkey

```typescript
import {
  PasskeyKeypair,
  BrowserPasskeyProvider,
  BrowserPasswordProviderOptions,
} from "@mysten/sui/keypairs/passkey";

const keypair = await PasskeyKeypair.getPasskeyInstance(
  new BrowserPasskeyProvider("My Sui App", {
    rpName: "My Sui App",
    rpId: window.location.hostname,
    authenticatorSelection: {
      authenticatorAttachment: "platform", // device biometric
      // or 'cross-platform' for security keys
      userVerification: "required",
    },
  } as BrowserPasswordProviderOptions)
);
```

## Usage (Same as Other Keypairs)

```typescript
// Get address
const publicKey = keypair.getPublicKey();
const address = publicKey.toSuiAddress();

// Sign message
const message = new TextEncoder().encode("Hello Sui");
const { signature } = await keypair.signPersonalMessage(message);

// Sign transaction
const txSignature = await keypair.signTransaction(txBytes);
```

## With Transactions

```typescript
import { Transaction } from "@mysten/sui/transactions";

const tx = new Transaction();
tx.moveCall({ target: "...", arguments: [] });

const { bytes, signature } = await tx.sign({
  client,
  signer: keypair, // passkey prompts biometric
});

await client.executeTransactionBlock({
  transactionBlock: bytes,
  signature,
});
```

## Multisig with Passkey

```typescript
import { MultiSigPublicKey } from "@mysten/sui/multisig";

const passkeyKeypair = await PasskeyKeypair.getPasskeyInstance(
  new BrowserPasskeyProvider("Sui Passkey", {
    rpName: "Sui Passkey",
    rpId: window.location.hostname,
  })
);

const multiSigPublicKey = MultiSigPublicKey.fromPublicKeys({
  threshold: 2,
  publicKeys: [
    { publicKey: passkeyKeypair.getPublicKey(), weight: 1 },
    { publicKey: ed25519Keypair.getPublicKey(), weight: 1 },
    { publicKey: secp256k1Keypair.getPublicKey(), weight: 1 },
  ],
});

const multisigAddress = multiSigPublicKey.toSuiAddress();
```

## Authenticator Options

| Option                    | Values           | Description                          |
| ------------------------- | ---------------- | ------------------------------------ |
| `authenticatorAttachment` | `platform`       | Device biometric (Touch ID, Face ID) |
|                           | `cross-platform` | Hardware security key (YubiKey)      |
| `userVerification`        | `required`       | Always verify user                   |
|                           | `preferred`      | Verify if available                  |
|                           | `discouraged`    | Skip verification                    |
| `residentKey`             | `required`       | Discoverable credential              |
|                           | `preferred`      | Discoverable if supported            |

## Browser Support

- Chrome 67+
- Safari 14+
- Firefox 60+
- Edge 79+

Requires HTTPS (except localhost).
