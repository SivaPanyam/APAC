import os
import dotenv
from google.adk import agents
# Relative import from the same app directory
try:
    from mcp_trip_app import tools
except ImportError:
    import tools

# Load any environment variables
dotenv.load_dotenv()

# Initialize the toolset
trip_toolset = tools.get_trip_mcp_toolset()

# Define the Agent using LlmAgent
root_agent = agents.LlmAgent(
    model='gemini-1.5-flash',
    name='root_agent',
    instruction="""
                Help the user plan a budget-friendly trip by combining insights from the following source:
                
                1. **Budget Trip Planner toolset:** Fetch structured trip data for hotels, places, and food for a given location and budget.

                Instructions:
                - Use 'get_budget_trip_data' tool with the user's location and budget.
                - Create a structured 1-day itinerary with summary, hotels, places, and food.
                - If the data is not available, ask for a different location or budget.
                - Always present the plan in a friendly way.
            """,
    tools=trip_toolset
)

# Export the agent for ADK web to recognize
agent = root_agent
