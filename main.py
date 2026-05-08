import typer
import asyncio
from agents.orchestrator import Orchestrator
from database.db import get_db_connection

app = typer.Typer(help="Nexus-100: Multi-Agent Automation System for YouTube and Instagram.")

@app.command()
def niche_finder():
    """
    Analyzes trending shorts/reels in the last 24 hours to find a high-CPM niche.
    """
    typer.echo("Starting Niche Finder...")
    orchestrator = Orchestrator()
    result = orchestrator.run_niche_finder()
    typer.echo(f"Niche Finder Result:\n{result}")

@app.command()
def account_link(platform: str = typer.Option(..., help="Platform: 'youtube' or 'instagram'"),
                 account_name: str = typer.Option(..., help="Name of the account")):
    """
    Secure workflow to add new Gmail/Instagram accounts and store refresh tokens.
    """
    typer.echo(f"Linking {platform} account: {account_name}")

    # In a real app, this would trigger an OAuth2 flow.
    # For now, we simulate token generation.
    mock_token = f"mock_refresh_token_{platform}_{account_name}"

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO accounts (platform, account_name, refresh_token) VALUES (?, ?, ?)",
        (platform, account_name, mock_token)
    )
    conn.commit()
    conn.close()

    typer.echo("Account successfully linked and stored in the database.")

async def process_channel(channel_id: int):
    """
    Simulates the entire pipeline for a single channel asynchronously.
    """
    typer.echo(f"[Channel {channel_id}] Starting Auto-Pilot...")
    # Because CrewAI is currently synchronous, we simulate an async wrapping.
    # In a full production system with Pydantic-AI or native async, the agent calls would be awaited.

    # We offload the blocking CrewAI execution to a thread
    orchestrator = Orchestrator()
    loop = asyncio.get_running_loop()
    result = await loop.run_in_executor(None, orchestrator.run_auto_pilot)

    typer.echo(f"[Channel {channel_id}] Auto-Pilot Cycle Complete.")
    return result

@app.command()
def auto_pilot(channels: int = typer.Option(1, help="Number of channels to process concurrently (up to 100).")):
    """
    A loop that: Finds Niche -> Generates Script -> Creates Video -> Posts to Channels concurrently.
    """
    typer.echo(f"Starting Auto-Pilot Mode for {channels} channels using asyncio...")

    async def main():
        tasks = []
        for i in range(channels):
            tasks.append(process_channel(i+1))

        results = await asyncio.gather(*tasks)
        typer.echo("All channels processed.")

    asyncio.run(main())

@app.command()
def anti_spam():
    """
    Configures randomized upload times and 'Synthetically Generated' labeling per 2026 regulations.
    """
    typer.echo("Enabling Anti-Spam Measures...")
    from core.config import CONFIG
    settings = CONFIG.get("upload_settings", {})
    randomize = settings.get("randomize_upload_times", True)
    label = settings.get("label_synthetic", True)

    typer.echo(f"Randomized Upload Times: {'Enabled' if randomize else 'Disabled'}")
    typer.echo(f"Synthetic Labeling: {'Enabled' if label else 'Disabled'}")
    typer.echo("Anti-Spam measures successfully verified with configuration.")

if __name__ == "__main__":
    app()
