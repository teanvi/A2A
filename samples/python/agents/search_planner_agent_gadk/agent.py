import json
import random
from typing import Any, List, Optional  # Import List and Optional

from google.adk.agents.llm_agent import LlmAgent
from google.adk.artifacts import InMemoryArtifactService
from google.adk.memory.in_memory_memory_service import InMemoryMemoryService
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.tools.tool_context import ToolContext
from task_manager import \
    AgentWithTaskManager  # Assuming this import is correct

# Local cache for search plans
search_plans = {}


def generate_search_terms(
    query: str,
    reason: str,
) -> dict[str, Any]:
    """Generate a set of search terms for a given query.

    Args:
        query (str): The user's research query.
        reason (str): Your reasoning for why this search is important to the query.

    Returns:
        dict[str, Any]: A dictionary containing the search plan with search terms.
    """
    # Generate a unique ID for this search plan
    plan_id = 'plan_id_' + str(random.randint(1000000, 9999999))
    
    # Store in local cache
    search_plans[plan_id] = {
        'query': query,
        'reason': reason,
        'status': 'generated'
    }
    
    return {
        'plan_id': plan_id,
        'query': query,
        'reason': reason,
    }


class SearchPlannerAgent(AgentWithTaskManager):
    """An agent that plans web searches to answer user queries."""

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
        return 'Planning web searches to answer your query...'

    def _build_agent(self) -> LlmAgent:
        """Builds the LLM agent for the search planner agent."""
        return LlmAgent(
            model='gemini-2.0-flash-001',
            name='search_planner_agent',
            description=(
                'This agent plans a set of web searches to best answer'
                ' user queries by generating relevant search terms.'
            ),
            instruction="""
    You are a helpful research assistant. Given a query, come up with a set of web searches to perform to best answer the query. Output between 5 and 20 terms to query for.

    For example, if the user asks "What are the latest developments in quantum computing?", you might suggest searches such as:
      1. "Recent breakthroughs in quantum computing 2025"
      2. "Quantum supremacy latest achievements"
      3. "Quantum error correction advances"
      4. "Top quantum computing companies research"
      5. "Quantum computing applications in real world"
      6. "Quantum bits vs classical bits comparison"
      7. "Quantum computing hardware improvements"
      8. "Quantum algorithm developments"
      
    Your goal is to help users conduct comprehensive research by suggesting diverse and targeted search terms that cover different aspects of their query.
    
    When responding, organize the search terms in a clear numbered list and briefly explain why each term would be helpful for the user's research.
    """,
            tools=[
                generate_search_terms,
            ],
        )
