from crewai import Agent
from agents.research import get_gemini_llm

def create_ops_agent():
    return Agent(
        role="Ops Agent",
        goal="Manage OAuth2 token rotation for 100 Google/Meta accounts with cooldown logic to prevent IP flagging.",
        backstory="A meticulous DevOps engineer focused on secure, rate-limited API interactions to keep infrastructure stealthy.",
        verbose=True,
        allow_delegation=False,
        llm=get_gemini_llm()
    )
