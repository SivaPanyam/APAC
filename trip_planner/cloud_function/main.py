import functions_framework
import os
import json
import google.generativeai as genai
from flask import jsonify

# 1. Local Data (MCP replacement for Cloud Function)
DATA = {
  "bangalore": {
    "low": {"hotels": ["Zostel"], "places": ["Cubbon Park"], "food": ["Udupi Cafe"]},
    "high": {"hotels": ["The Leela"], "places": ["Bangalore Palace"], "food": ["Sunny's"]}
  },
  "delhi": {
    "low": {"hotels": ["Smyle Inn"], "places": ["Red Fort"], "food": ["Karim's"]},
    "high": {"hotels": ["The Oberoi"], "places": ["Qutub Minar"], "food": ["Indian Accent"]}
  }
}

# 2. Configure Gemini
genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

@functions_framework.http
def plan_trip(request):
    """HTTP Cloud Function."""
    request_json = request.get_json(silent=True)
    
    location = request_json.get('location', 'bangalore').lower()
    budget = request_json.get('budget', 'low').lower()
    
    # Get Data
    trip_data = DATA.get(location, {}).get(budget)
    if not trip_data:
        return jsonify({"error": "Data not found"}), 404
        
    # Generate Plan with Gemini
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = f"Plan a 1-day trip to {location} with a {budget} budget using this data: {json.dumps(trip_data)}. Return JSON."
    
    try:
        response = model.generate_content(prompt, generation_config={"response_mime_type": "application/json"})
        return jsonify(json.loads(response.text))
    except Exception as e:
        return jsonify({"error": str(e)}), 500
