from crewai import Agent, LLM
from agents.tools import find_niche_tool
from core.config import get_api_key

def get_gemini_llm():
    return LLM(model="gemini/gemini-1.5-flash", api_key=get_api_key("gemini_api") or "dummy_key")

def create_research_agent():
    return Agent(
        role="Research Agent",
        goal="Identify high-CPM, low-competition niches from YouTube trending data and Google Trends.",
        backstory="An expert data analyst specializing in YouTube and Google Trends to uncover hidden gems in the social media space.",
        verbose=True,
        allow_delegation=False,
        tools=[find_niche_tool],
        llm=get_gemini_llm()
    )
