from crewai import Agent
from agents.tools import generate_video_tool
from agents.research import get_gemini_llm

def create_production_agent():
    return Agent(
        role="Production Agent",
        goal="Programmatically generate videos using AI voiceovers and stock footage.",
        backstory="A seasoned video editor who uses code (MoviePy, gTTS) to assemble engaging videos automatically.",
        verbose=True,
        allow_delegation=False,
        tools=[generate_video_tool],
        llm=get_gemini_llm()
    )
