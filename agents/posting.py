from crewai import Agent
from agents.tools import post_video_tool
from agents.research import get_gemini_llm

def create_posting_agent():
    return Agent(
        role="Posting Agent",
        goal="Handle scheduled uploads to YouTube and Instagram with randomized times.",
        backstory="A reliable social media manager who strictly adheres to content calendars and anti-spam regulations (synthetic labels).",
        verbose=True,
        allow_delegation=False,
        tools=[post_video_tool],
        llm=get_gemini_llm()
    )
