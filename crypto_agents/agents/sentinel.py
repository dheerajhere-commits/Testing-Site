from typing import List, Dict
from .base_agent import BaseAgent
import random

class SentinelAgent(BaseAgent):
    def __init__(self, wallets: List[str], floor: float):
        super().__init__("Sentinel")
        self.wallets = wallets
        self.floor = floor

    def monitor(self) -> List[Dict]:
        """Simulate polling a blockchain RPC for balances."""
        events = []
        for wallet in self.wallets:
            # Simulate fetching a balance (for simulation purposes, mostly above floor)
            simulated_balance = random.uniform(self.floor - 200, self.floor + 5000)
            if simulated_balance < self.floor:
                events.append({"type": "BALANCE_WARNING", "wallet": wallet, "balance": simulated_balance})
                self.log(f"WARNING: {wallet} balance (${simulated_balance:.2f}) is below floor (${self.floor:.2f})!")
            else:
                events.append({"type": "BALANCE_STABLE", "wallet": wallet, "balance": simulated_balance})
        return events
