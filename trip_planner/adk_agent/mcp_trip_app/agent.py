import os
import dotenv
from google.adk import agents
# Local folder import
import mcp_trip_app.tools as tools

# Load environment
dotenv.load_dotenv()

# Initialize toolset
trip_toolset = tools.get_trip_mcp_toolset()

# Define the Agent
agent = agents.LlmAgent(
    model='gemini-1.5-flash',
    name='root_agent',
    instruction="""
                You are a helpful AI Budget Trip Planner. 
                Your goal is to help users plan a 1-day trip based on their location and budget.
                
                Workflow:
                1. Use 'get_budget_trip_data' to fetch data for the location and budget.
                2. Create a friendly 1-day itinerary with summary, hotels, places, and food.
                3. If no data is found, ask for another location/budget.
            """,
    tools=trip_toolset
)

# Global object for ADK web to detect
root_agent = agent
