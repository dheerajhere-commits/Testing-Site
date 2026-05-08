import json
import os
from datetime import datetime
from .base_agent import BaseAgent

class GovernorAgent(BaseAgent):
    def __init__(self, ledger_path: str):
        super().__init__("Governor")
        self.ledger_path = ledger_path
        self._ensure_ledger()

    def _ensure_ledger(self):
        if not os.path.exists(self.ledger_path):
            initial_state = {
                "last_updated": datetime.now().isoformat(),
                "agents": {
                    "Executor": {"score": 100, "status": "active", "cooldown_until": None, "history": []},
                    "Solver": {"score": 100, "status": "active", "cooldown_until": None, "history": []}
                }
            }
            with open(self.ledger_path, "w") as f:
                json.dump(initial_state, f, indent=2)

    def process_event(self, event: dict):
        # A simple event processor logic
        if event["type"] == "CLAIM_SUCCESS":
            self._update_score("Executor", 10, "reward", "Successful claim transaction")
        elif event["type"] == "CLAIM_FAILED":
            self._update_score("Executor", -15, "penalty", "Failed transaction (wasted gas)")
        elif event["type"] == "BALANCE_WARNING":
             self.log(f"Noted balance warning for {event['wallet']}")

    def _update_score(self, agent_name: str, delta: int, action: str, reason: str):
        with open(self.ledger_path, "r") as f:
            ledger = json.load(f)

        if agent_name in ledger["agents"]:
            ledger["agents"][agent_name]["score"] += delta
            ledger["agents"][agent_name]["history"].append({
                "timestamp": datetime.now().isoformat(),
                "action": action,
                "amount": delta,
                "reason": reason
            })
            ledger["last_updated"] = datetime.now().isoformat()

            with open(self.ledger_path, "w") as f:
                json.dump(ledger, f, indent=2)

            self.log(f"Updated {agent_name} score by {delta} ({reason})")
