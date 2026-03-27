from google import adk
import os
import requests
import json

# Internal MCP server URL
MCP_URL = os.environ.get("MCP_URL", "http://localhost:8081/get-trip")

# Define the Tool for the Agent
@adk.tool
def get_budget_trip_data(location: str, budget: str) -> str:
    """
    Fetches structured budget trip data (hotels, places, food) for a specific location and budget level.
    Args:
        location: The city or destination (e.g., 'bangalore', 'delhi').
        budget: The budget level ('low' or 'high').
    """
    try:
        response = requests.post(MCP_URL, json={"location": location, "budget": budget})
        if response.status_code == 200:
            return json.dumps(response.json())
        return f"Error: No data found for {location} with {budget} budget."
    except Exception as e:
        return f"Connection Error: {str(e)}"

# Define the Agent
agent = adk.Agent(
    name="Budget Trip Planner",
    instructions="""
    You are a helpful AI Budget Trip Planner. 
    Your goal is to help users plan a 1-day trip based on their location and budget.
    
    Workflow:
    1. Use the 'get_budget_trip_data' tool to fetch actual data for the location and budget.
    2. Based on the data returned (hotels, places, food), create a creative 1-day itinerary.
    3. If the tool returns an error, inform the user politely.
    
    Always present the final plan in a structured and friendly way.
    """,
    model="gemini-1.5-flash",
    tools=[get_budget_trip_data]
)

if __name__ == "__main__":
    adk.run(agent)
