from crewai import Agent
from agents.tools import generate_script_tool
from agents.research import get_gemini_llm

def create_creative_agent():
    return Agent(
        role="Creative Agent",
        goal="Generate viral scripts and SEO-optimized metadata (Titles, Tags, Descriptions).",
        backstory="A highly creative copywriter and SEO expert who knows exactly how to hook an audience and rank high in search algorithms.",
        verbose=True,
        allow_delegation=False,
        tools=[generate_script_tool],
        llm=get_gemini_llm()
    )
