# Nautilus

Secure off-chain computation framework using AWS Nitro Enclaves (TEE).

## Overview

Nautilus enables verifiable off-chain computation on Sui. Code runs in isolated AWS Nitro Enclaves with cryptographic attestation proving execution integrity.

## Architecture

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────┐
│   Sui Client    │────▶│  Nautilus API    │────▶│   Enclave   │
│                 │◀────│  (HTTP Server)   │◀────│   (TEE)     │
└─────────────────┘     └──────────────────┘     └─────────────┘
                                │
                                ▼
                        ┌──────────────────┐
                        │   Sui Network    │
                        │  (Attestation)   │
                        └──────────────────┘
```

## Enclave API Endpoints

```
GET  /health_check     - Check enclave status
GET  /get_attestation  - Get signed attestation document
POST /process_data     - Execute computation
```

## Client Integration

```typescript
// Health check
const health = await fetch(`${ENCLAVE_URL}/health_check`);

// Get attestation for on-chain registration
const attestation = await fetch(`${ENCLAVE_URL}/get_attestation`);
const { publicKey, attestationDoc } = await attestation.json();

// Process data
const result = await fetch(`${ENCLAVE_URL}/process_data`, {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    payload: { location: "San Francisco" },
  }),
});
const { data, signature } = await result.json();
```

## On-Chain Registration

```bash
# Deploy enclave package
cd move/enclave
sui move build
sui client publish
# Record ENCLAVE_PACKAGE_ID

# Deploy app logic
cd ../app
sui move build
sui client publish
# Record CAP_OBJECT_ID, ENCLAVE_CONFIG_OBJECT_ID
```

## Move Verification

```move
module app::weather;

use enclave::attestation::{Self, EnclaveConfig};

public fun verify_and_use_data(
    config: &EnclaveConfig,
    data: vector<u8>,
    signature: vector<u8>,
) {
    // Verify signature from registered enclave
    assert!(
        attestation::verify(config, data, signature),
        EInvalidSignature
    );

    // Use verified data
    let weather = parse_weather(data);
    // ...
}
```

## Use Cases

| Use Case        | Description                              |
| --------------- | ---------------------------------------- |
| Oracles         | Fetch external data with proof of source |
| Private Compute | Process sensitive data off-chain         |
| AI/ML Inference | Run models with verifiable results       |
| Cross-chain     | Bridge data with attestation             |
| Randomness      | Generate verifiable random numbers       |

## Enclave Server (Rust)

```rust
// src/nautilus-server/app.rs
// Custom computation logic

async fn process_data(payload: Payload) -> Result<SignedResponse> {
    // Fetch external data
    let data = fetch_weather(&payload.location).await?;

    // Sign with enclave key
    let signature = enclave_sign(&data)?;

    Ok(SignedResponse { data, signature })
}
```

## Security Properties

- **Isolation**: Code runs in hardware-isolated enclave
- **Attestation**: Cryptographic proof of code integrity
- **Confidentiality**: Data encrypted in transit and at rest
- **Verifiability**: On-chain verification of enclave signatures

## Deployment

1. Build enclave image (reproducible)
2. Deploy to AWS Nitro
3. Register enclave public key on Sui
4. Clients verify attestation before trusting

## Resources

- [Nautilus GitHub](https://github.com/mystenlabs/nautilus)
- [AWS Nitro Enclaves](https://aws.amazon.com/ec2/nitro/nitro-enclaves/)
