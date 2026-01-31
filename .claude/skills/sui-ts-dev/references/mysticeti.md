# Mysticeti

DAG-based Byzantine consensus protocol powering Sui.

## Overview

Mysticeti is Sui's consensus layer - a high-throughput, low-latency protocol using Directed Acyclic Graph (DAG) structure instead of traditional linear chains.

## Key Properties

| Property        | Value                                  |
| --------------- | -------------------------------------- |
| Latency         | 3 message rounds (theoretical minimum) |
| Throughput      | 200k+ TPS                              |
| WAN Latency     | ~0.5s consensus commit                 |
| Fault Tolerance | Byzantine (up to 1/3 malicious)        |

## How It Works

### DAG Structure

```
Round 3:  [B3-1] ─────┬───── [B3-2] ─────┬───── [B3-3]
              │       │          │       │          │
Round 2:  [B2-1] ─────┼───── [B2-2] ─────┼───── [B2-3]
              │       │          │       │          │
Round 1:  [B1-1] ─────┴───── [B1-2] ─────┴───── [B1-3]
          Val-1            Val-2            Val-3
```

- Multiple validators propose blocks in parallel
- Blocks reference previous round blocks (DAG edges)
- No explicit block certification needed

### Commit Rule

1. Validators propose blocks referencing prior blocks
2. Implicit commitment through DAG structure
3. Leader blocks anchor commit decisions
4. 3 rounds to finality (matches pBFT minimum)

## Advantages Over Traditional BFT

| Feature        | Traditional BFT | Mysticeti            |
| -------------- | --------------- | -------------------- |
| Block proposal | Sequential      | Parallel             |
| Certification  | Explicit votes  | Implicit DAG         |
| Network usage  | Partial         | Full bandwidth       |
| Leader failure | High latency    | Graceful degradation |

## Transaction Flow

```
1. Client submits transaction
2. Validators include in DAG blocks
3. Consensus orders transactions
4. Execution parallelized by object
5. Checkpoint formed per commit
```

## Shared Object Handling

- Consensus determines transaction order for shared objects
- Owned objects bypass consensus (fast path)
- Execution parallelized across different shared objects

## Censorship Resistance

- Multiple validators propose simultaneously
- Transaction included if any honest validator sees it
- No single leader bottleneck

## Performance Optimizations

### Mysticeti-C (Core)

- Uncertified DAG blocks
- Novel commit rule without delays
- Optimal steady-state latency

### Mysticeti-FPC (Fast Path)

- Minimizes signatures for simple transactions
- Integrates fast path into DAG
- Frees resources for complex transactions

## Integration with Sui

```
┌─────────────────────────────────────────────────┐
│                   Sui Network                    │
├─────────────────────────────────────────────────┤
│  Owned Objects    │    Shared Objects           │
│  (Fast Path)      │    (Mysticeti Consensus)    │
│  - No consensus   │    - DAG ordering           │
│  - ~400ms         │    - ~500ms                 │
└─────────────────────────────────────────────────┘
```

## Research

- [Mysticeti Paper](https://arxiv.org/abs/2310.14821)
- Achieves theoretical lower bound for Byzantine consensus
- Proven safe and live under Byzantine conditions
