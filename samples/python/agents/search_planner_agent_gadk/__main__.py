import logging
import os

import click
from agent import SearchPlannerAgent
from common.server import A2AServer
from common.types import (AgentCapabilities, AgentCard, AgentSkill,
                          MissingAPIKeyError)
from dotenv import load_dotenv
from task_manager import AgentTaskManager

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@click.command()
@click.option('--host', default='localhost')
@click.option('--port', default=30001)
def main(host, port):
    try:
        # Check for API key only if Vertex AI is not configured
        if not os.getenv('GOOGLE_GENAI_USE_VERTEXAI') == 'TRUE':
            if not os.getenv('GOOGLE_API_KEY'):
                raise MissingAPIKeyError(
                    'GOOGLE_API_KEY environment variable not set and GOOGLE_GENAI_USE_VERTEXAI is not TRUE.'
                )

        capabilities = AgentCapabilities(streaming=True)
        skill = AgentSkill(
            id='plan_web_searches',
            name='Web Search Planner Tool',
            description='Given a query, comes up with a set of web searches to perform to best answer the query.',
            tags=['search', 'research', 'web'],
            examples=[
                'What are the latest developments in quantum computing?',
                'How does climate change affect marine ecosystems?'
            ],
        )
        agent_card = AgentCard(
            name='Search Planner Agent',
            description='A helpful research assistant that plans a set of web searches to answer your query. Given a query, it provides 5 to 20 search terms to help you find the best answer.',
            url=f'http://{host}:{port}/',
            version='1.0.0',
            defaultInputModes=SearchPlannerAgent.SUPPORTED_CONTENT_TYPES,
            defaultOutputModes=SearchPlannerAgent.SUPPORTED_CONTENT_TYPES,
            capabilities=capabilities,
            skills=[skill],
        )
        server = A2AServer(
            agent_card=agent_card,
            task_manager=AgentTaskManager(agent=SearchPlannerAgent()),
            host=host,
            port=port,
        )
        server.start()
    except MissingAPIKeyError as e:
        logger.error(f'Error: {e}')
        exit(1)
    except Exception as e:
        logger.error(f'An error occurred during server startup: {e}')
        exit(1)


if __name__ == '__main__':
    main()
