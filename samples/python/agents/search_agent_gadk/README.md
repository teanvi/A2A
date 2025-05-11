## ADK Agent

### Agent System Prompt
You are a research assistant. Given a search term, you search the web for that term and produce a concise summary of the results. The summary must 2-3 paragraphs and less than 300 words. Capture the main points. Write succinctly, no need to have complete sentences or good grammar. This will be consumed by someone synthesizing a report, so its vital you capture the essence and ignore any fluff. Do not include any additional commentary other than the summary itself.

This sample uses the Agent Development Kit (ADK) to create an Search agent that can search the web
for a term and produce a summary of the results.

## ADK Search Example

### Additional requirements when using the google_search tool
**When you use grounding with Google Search, and you receive Search suggestions in your response, you must display the Search suggestions in production and in your applications. For more information on grounding with Google Search, see Grounding with Google Search documentation for Google AI Studio or Vertex AI. The UI code (HTML) is returned in the Gemini response as renderedContent, and you will need to show the HTML in your app, in accordance with the policy.**

```python
from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.tools import google_search
from google.genai import types

APP_NAME="google_search_agent"
USER_ID="user1234"
SESSION_ID="1234"


root_agent = Agent(
    name="basic_search_agent",
    model="gemini-2.0-flash",
    description="Agent to answer questions using Google Search.",
    instruction="I can answer your questions by searching the internet. Just ask me anything!",
    # google_search is a pre-built tool which allows the agent to perform Google searches.
    tools=[google_search]
)

# Session and Runner
session_service = InMemorySessionService()
session = session_service.create_session(app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID)
runner = Runner(agent=root_agent, app_name=APP_NAME, session_service=session_service)


# Agent Interaction
def call_agent(query):
    """
    Helper function to call the agent with a query.
    """
    content = types.Content(role='user', parts=[types.Part(text=query)])
    events = runner.run(user_id=USER_ID, session_id=SESSION_ID, new_message=content)

    for event in events:
        if event.is_final_response():
            final_response = event.content.parts[0].text
            print("Agent Response: ", final_response)

call_agent("what's the latest ai news?")
```


## Prerequisites

- Python 3.9 or higher
- [UV](https://docs.astral.sh/uv/)
- Access to an LLM and API Key


## Running the Sample

1. Navigate to the samples directory:
    ```bash
    cd samples/python/agents/search_agent_gadk
    ```
2. Create an environment file with your API key:

   ```bash
   echo "GOOGLE_API_KEY=your_api_key_here" > .env
   ```

4. Run an agent:
    ```bash
    uv run .
    ```

5. In a separate terminal, run the A2A client:
    ```
    # Connect to the agent (specify the agent URL with correct port)
    cd samples/python/hosts/cli
    uv run . --agent http://localhost:30002

    # If you changed the port when starting the agent, use that port instead
    # uv run . --agent http://localhost:YOUR_PORT
    ```
