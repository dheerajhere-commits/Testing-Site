import typer
import json
import os
from crypto_agents.core.simulation import run_simulation
from crypto_agents.core.config import LEDGER_PATH

app = typer.Typer(help="Multi-Agent CLI for Autonomous DeFi Portfolio Management")

@app.command()
def run(
    simulation: bool = typer.Option(True, "--sim/--live", help="Run in simulation mode (Anvil/Hardhat) or Live (Mainnet)"),
    wallets: int = typer.Option(6, help="Number of wallet addresses to manage"),
    floor: float = typer.Option(1000.0, help="Minimum liquidity floor in USD per wallet")
):
    """Start the multi-agent system."""
    typer.echo(f"Starting Multi-Agent System...")
    mode = "SIMULATION" if simulation else "LIVE MAINNET (DANGER)"
    typer.echo(f"Mode: {mode}")
    typer.echo(f"Monitoring {wallets} wallets with a floor of ${floor:,.2f}")

    if not simulation:
        typer.echo("WARNING: Live mode selected. Proceed with caution.", err=True)
        return

    # Generate dummy wallet addresses for simulation
    sim_wallets = [f"0xSimulatedWallet{i:04d}" for i in range(1, wallets + 1)]

    # Run the simulation loop
    run_simulation(sim_wallets, floor)

@app.command()
def status():
    """Check the current status of the agents and the reward/penalty ledger."""
    if not os.path.exists(LEDGER_PATH):
        typer.echo("No ledger found. Has the simulation run yet?")
        return

    with open(LEDGER_PATH, "r") as f:
        ledger = json.load(f)

    typer.echo("\n--- Agent Ledger Status ---")
    typer.echo(f"Last Updated: {ledger['last_updated']}")
    for agent_name, data in ledger["agents"].items():
        typer.echo(f"\nAgent: {agent_name}")
        typer.echo(f"  Score: {data['score']}")
        typer.echo(f"  Status: {data['status']}")
        typer.echo(f"  Recent History:")
        for entry in data["history"][-3:]: # Show last 3
            typer.echo(f"    - {entry['action'].upper()}: {entry['amount']} ({entry['reason']})")

@app.command()
def solve(puzzle_url: str):
    """Manually trigger the Solver agent for a specific CTF or puzzle."""
    typer.echo(f"Dispatching Solver agent to analyze: {puzzle_url}")
    from crypto_agents.agents.solver import SolverAgent
    solver = SolverAgent()
    solver.analyze_puzzle(puzzle_url)

if __name__ == "__main__":
    app()
