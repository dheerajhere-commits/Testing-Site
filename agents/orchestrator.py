from crewai import Crew, Task
from agents.research import create_research_agent
from agents.creative import create_creative_agent
from agents.production import create_production_agent
from agents.ops import create_ops_agent
from agents.posting import create_posting_agent

class Orchestrator:
    def __init__(self):
        self.research_agent = create_research_agent()
        self.creative_agent = create_creative_agent()
        self.production_agent = create_production_agent()
        self.ops_agent = create_ops_agent()
        self.posting_agent = create_posting_agent()

    def run_niche_finder(self):
        task = Task(
            description="Analyze trending shorts/reels in the last 24 hours to find a high-CPM niche.",
            expected_output="A brief report detailing a recommended high-CPM niche with low competition.",
            agent=self.research_agent
        )
        crew = Crew(
            agents=[self.research_agent],
            tasks=[task],
            verbose=True
        )
        return crew.kickoff()

    def run_auto_pilot(self):
        # Step 1: Find Niche
        research_task = Task(
            description="Find a high-CPM, low-competition niche for a new short/reel.",
            expected_output="The chosen niche name.",
            agent=self.research_agent
        )

        # Step 2: Generate Script
        creative_task = Task(
            description="Based on the chosen niche, generate a viral script and SEO metadata (Title, Tags, Description).",
            expected_output="A JSON-like string containing 'script', 'title', 'tags', and 'description'.",
            agent=self.creative_agent
        )

        # Step 3: Create Video
        production_task = Task(
            description="Use the generated script to programmatically create a video using stock footage and AI voiceover. Output the path to the video.",
            expected_output="The file path of the generated video.",
            agent=self.production_agent
        )

        # Step 4: Schedule and Post
        posting_task = Task(
            description="Take the generated video path and metadata, and schedule uploads across multiple accounts using anti-spam delays.",
            expected_output="A summary of scheduled/posted videos.",
            agent=self.posting_agent
        )

        crew = Crew(
            agents=[self.research_agent, self.creative_agent, self.production_agent, self.posting_agent],
            tasks=[research_task, creative_task, production_task, posting_task],
            verbose=True
        )
        return crew.kickoff()
