import json
import random
from typing import Any, List, Optional  # Import List and Optional

from google.adk.agents import Agent
from google.adk.artifacts import InMemoryArtifactService
from google.adk.memory.in_memory_memory_service import InMemoryMemoryService
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.tools import google_search
from google.adk.tools.tool_context import ToolContext
from task_manager import \
    AgentWithTaskManager  # Assuming this import is correct

# Local cache for search results
search_results = {}


def perform_search(
    query: str,
) -> dict[str, Any]:
    """Perform a web search for a query.

    Args:
        query (str): The search term to look up.

    Returns:
        dict[str, Any]: A dictionary containing the search results.
    """
    # Generate a unique ID for this search
    search_id = 'search_id_' + str(random.randint(1000000, 9999999))
    
    # Store in local cache
    search_results[search_id] = {
        'query': query,
        'status': 'submitted'
    }
    
    return {
        'search_id': search_id,
        'query': query,
    }


class SearchAgent(AgentWithTaskManager):
    """An agent that searches the web for a term and produces a summary of the results."""

    SUPPORTED_CONTENT_TYPES = ['text', 'text/plain']

    def __init__(self):
        self._agent = self._build_agent()
        self._user_id = 'remote_agent'
        self._runner = Runner(
            app_name=self._agent.name,
            agent=self._agent,
            artifact_service=InMemoryArtifactService(),
            session_service=InMemorySessionService(),
            memory_service=InMemoryMemoryService(),
        )

    def get_processing_message(self) -> str:
        return 'Searching the web to answer your query...'

    def _build_agent(self) -> Agent:
        """Builds the agent for the search agent."""
        return Agent(
            model='gemini-2.0-flash',
            name='search_agent',
            description=(
                'This agent searches the web for a term and produces a concise'
                ' summary of the results.'
            ),
            instruction="""
    You are a research assistant. Given a search term, you search the web for that term and produce a concise summary of the results. 
    The summary must 2-3 paragraphs and less than 300 words. Capture the main points. Write succinctly, no need to have complete sentences 
    or good grammar. This will be consumed by someone synthesizing a report, so its vital you capture the essence and ignore any fluff. 
    Do not include any additional commentary other than the summary itself.
    """,
            # google_search is a pre-built tool which allows the agent to perform Google searches.
            tools=[google_search],
        )
