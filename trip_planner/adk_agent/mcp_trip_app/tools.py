import os
import requests
import json
import dotenv
from google.adk import MCPToolset, StreamableHTTPConnectionParams

# Internal MCP server URL
MCP_URL = os.environ.get("MCP_URL", "http://127.0.0.1:8081/get-trip")

def get_trip_mcp_toolset():
    """
    Connects to the local FastAPI MCP server using a tool that interacts with it.
    Since the current version of adk.tool handles the function wrapping, we will define it here.
    """
    # This matches the pattern in tools.py to keep tools logic separate.
    return [get_budget_trip_data]

def get_budget_trip_data(location: str, budget: str) -> str:
    """
    Fetches structured budget trip data (hotels, places, food) for a specific location and budget level.
    Args:
        location: The city or destination (e.g., 'bangalore', 'delhi').
        budget: The budget level ('low' or 'high').
    """
    try:
        # Connect to our local MCP-style FastAPI server
        response = requests.post(MCP_URL, json={"location": location, "budget": budget}, timeout=10)
        if response.status_code == 200:
            return json.dumps(response.json())
        return f"Error: No data found for {location} with {budget} budget."
    except Exception as e:
        return f"Connection Error connecting to MCP: {str(e)}"
