import os
import json
import requests
import google.generativeai as genai
from typing import Dict, Any

# Configure Gemini
# Ensure GOOGLE_API_KEY is set in environment
genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

# Internal MCP server URL (assumed to be on localhost:8081)
MCP_URL = os.environ.get("MCP_URL", "http://localhost:8081/get-trip")

def fetch_mcp_data(location: str, budget: str) -> Dict[str, Any]:
    try:
        response = requests.post(MCP_URL, json={"location": location, "budget": budget})
        if response.status_code == 200:
            return response.json()
        return {}
    except requests.exceptions.RequestException:
        return {}

def plan_trip_with_gemini(location: str, budget: str) -> Dict[str, Any]:
    # 1. Fetch data from MCP
    mcp_data = fetch_mcp_data(location, budget)
    
    if not mcp_data:
        return {"error": f"No budget-friendly data found for {location}."}
    
    # 2. Setup Gemini Prompt
    model = genai.GenerativeModel("gemini-1.5-flash")
    
    prompt = f"""
    You are a travel assistant for AI Budget Trip Planner.
    Use the following structured trip data from an external MCP service:
    
    Data: {json.dumps(mcp_data)}
    Location: {location}
    Budget: {budget}
    
    Requirements:
    - Generate a 1-day trip plan.
    - Include: plan summary, list of hotels, list of places, and list of food.
    - Output must be in strictly valid JSON format.
    
    Expected JSON format:
    {{
      "plan": "detailed plan description",
      "hotels": ["hotel1", "hotel2"],
      "places": ["place1", "place2"],
      "food": ["food1", "food2"]
    }}
    """
    
    try:
        # Use generation_config for strict JSON output if available or just clean response
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(response_mime_type="application/json")
        )
        
        # Parse JSON output from Gemini
        result = json.loads(response.text)
        return result
    except Exception as e:
        return {"error": f"Failed to generate plan: {str(e)}"}
