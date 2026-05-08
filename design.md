# Multi-Agent DeFi Portfolio Management & CTF Solver

## Directory Structure

```
crypto_agents/
├── main.py                  # CLI entry point using Typer/Click
├── .env                     # Sensitive API keys and wallet addresses
├── .env.example             # Template for .env
├── agents/
│   ├── __init__.py
│   ├── base_agent.py        # Abstract base class for agents
│   ├── sentinel.py          # Monitors wallet balances
│   ├── solver.py            # Scrapes and solves crypto puzzles/CTFs
│   ├── executor.py          # Signs and broadcasts transactions (Web3.py)
│   └── governor.py          # Manages reward/penalty ledger and agent scores
├── core/
│   ├── __init__.py
│   ├── config.py            # Loads environment variables
│   ├── simulation.py        # Logic for Hardhat/Anvil simulation mode
│   ├── communication.py     # Inter-agent message bus (e.g., simple queue)
│   └── ledger.py            # Interfaces with the reward/penalty JSON ledger
└── data/
    └── ledger.json          # State file for agent scores and history
```

## Sentinel and Governor Communication Protocol

The Sentinel agent is responsible for monitoring 6+ distinct wallet addresses and ensuring their balances stay above a specified floor (e.g., $1,000 equivalent). The Governor agent maintains the overall system state, including assigning rewards/penalties to other agents based on performance.

### Message Flow

1. **Monitoring Loop**: The Sentinel agent runs a continuous loop (or scheduled task), polling a blockchain RPC (like Alchemy or Etherscan API) for the balance of all registered wallets.
2. **State Evaluation**: The Sentinel compares the fetched balances against the configured floor ($1,000).
3. **Event Generation**:
   - If a wallet's balance drops below the floor, the Sentinel emits a `BALANCE_WARNING` event.
   - If a wallet maintains or restores its balance above the floor, the Sentinel emits a `BALANCE_STABLE` event.
4. **Message Dispatch**: The Sentinel serializes this event (e.g., as JSON or a Python dataclass) and pushes it to the central inter-agent message bus (managed in `core.communication`).
5. **Governor Ingestion**: The Governor agent listens to the message bus for events related to system health and agent performance.
6. **Action/Ledger Update**:
   - Upon receiving a `BALANCE_WARNING`, the Governor may penalize the Executor agent (if the drop was due to excessive gas waste) or alert the user.
   - Upon receiving a `BALANCE_STABLE` (especially after a recovery), the Governor may reward the responsible agents.

### JSON Schema for Reward/Penalty Ledger

The Governor maintains a ledger tracking the performance scores of all agents.

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Agent Reward/Penalty Ledger",
  "type": "object",
  "properties": {
    "last_updated": {
      "type": "string",
      "format": "date-time"
    },
    "agents": {
      "type": "object",
      "patternProperties": {
        "^[a-zA-Z0-9_]+$": {
          "type": "object",
          "properties": {
            "score": {
              "type": "number",
              "description": "Current performance score of the agent"
            },
            "status": {
              "type": "string",
              "enum": ["active", "cooldown", "suspended"]
            },
            "cooldown_until": {
              "type": ["string", "null"],
              "format": "date-time"
            },
            "history": {
              "type": "array",
              "items": {
                "type": "object",
                "properties": {
                  "timestamp": {
                    "type": "string",
                    "format": "date-time"
                  },
                  "action": {
                    "type": "string",
                    "enum": ["reward", "penalty"]
                  },
                  "amount": {
                    "type": "number"
                  },
                  "reason": {
                    "type": "string"
                  }
                },
                "required": ["timestamp", "action", "amount", "reason"]
              }
            }
          },
          "required": ["score", "status", "history"]
        }
      }
    }
  },
  "required": ["last_updated", "agents"]
}
```
