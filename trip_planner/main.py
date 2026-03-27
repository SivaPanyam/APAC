from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from agent import plan_trip_with_gemini

app = FastAPI(title="AI Budget Trip Planner Agent")

class TripRequest(BaseModel):
    location: str
    budget: str

@app.get("/")
async def health_check():
    return {"status": "ok", "message": "Agent server is running"}

@app.post("/plan-trip")
async def plan_trip(request: TripRequest):
    result = plan_trip_with_gemini(request.location, request.budget)
    
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    
    return result

if __name__ == "__main__":
    import uvicorn
    # Main entry point for Cloud Run on port 8080
    uvicorn.run(app, host="0.0.0.0", port=8080)
