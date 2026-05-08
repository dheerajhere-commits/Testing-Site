import time
from typing import List
from crypto_agents.agents.sentinel import SentinelAgent
from crypto_agents.agents.solver import SolverAgent
from crypto_agents.agents.executor import ExecutorAgent
from crypto_agents.agents.governor import GovernorAgent
from crypto_agents.core.config import LEDGER_PATH

def run_simulation(wallets: List[str], floor: float, cycles: int = 3):
    sentinel = SentinelAgent(wallets, floor)
    solver = SolverAgent()
    executor = ExecutorAgent()
    governor = GovernorAgent(LEDGER_PATH)

    print("\n--- Starting Simulation ---")
    for cycle in range(1, cycles + 1):
        print(f"\nCycle {cycle}:")

        # 1. Sentinel monitors wallets
        events = sentinel.monitor()
        for event in events:
            governor.process_event(event)

        # 2. Solver attempts a puzzle
        if solver.analyze_puzzle(f"https://simulated-ctf.local/puzzle_{cycle}"):
            # 3. If solved, Executor claims
            target_wallet = wallets[cycle % len(wallets)]
            if executor.execute_claim(target_wallet, reward_amount=250.0):
                 governor.process_event({"type": "CLAIM_SUCCESS"})
            else:
                 governor.process_event({"type": "CLAIM_FAILED"})

        time.sleep(1) # Simulate time passing

    print("\n--- Simulation Complete ---")
