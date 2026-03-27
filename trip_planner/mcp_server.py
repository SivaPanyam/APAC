from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
import os

app = FastAPI(title="MCP Trip Data Server")

class TripRequest(BaseModel):
    location: str
    budget: str

# Load data.json
DATA_PATH = os.path.join(os.path.dirname(__file__), "data.json")

def load_data():
    with open(DATA_PATH, "r") as f:
        return json.load(f)

@app.post("/get-trip")
async def get_trip(request: TripRequest):
    data = load_data()
    location = request.location.lower()
    budget = request.budget.lower()
    
    if location in data and budget in data[location]:
        return data[location][budget]
    else:
        raise HTTPException(status_code=404, detail="Trip data not found for this location and budget.")

if __name__ == "__main__":
    import uvicorn
    # Use port 8081 for internal MCP
    uvicorn.run(app, host="0.0.0.0", port=8081)
