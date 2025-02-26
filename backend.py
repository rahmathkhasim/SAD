from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel
from typing import Dict
import uvicorn

app = FastAPI()

# In-memory storage for pending requests
pending_requests: Dict[str, Dict] = {}

class ApprovalRequest(BaseModel):
    visitor_name: str
    visitor_phone: str
    resident_email: str
    status: str = "pending"

@app.post("/request/{request_id}")
def create_request(request_id: str, request: ApprovalRequest):
    pending_requests[request_id] = request.dict()
    return {"message": "Request created", "request_id": request_id}

@app.get("/approve/{request_id}")
def approve_request(request_id: str):
    if request_id not in pending_requests:
        raise HTTPException(status_code=404, detail="Request not found")
    pending_requests[request_id]["status"] = "approved"
    return {"message": "Request approved", "request_id": request_id}

@app.get("/deny/{request_id}")
def deny_request(request_id: str):
    if request_id not in pending_requests:
        raise HTTPException(status_code=404, detail="Request not found")
    pending_requests[request_id]["status"] = "denied"
    return {"message": "Request denied", "request_id": request_id}

@app.get("/blacklist/{request_id}")
def blacklist_request(request_id: str):
    if request_id not in pending_requests:
        raise HTTPException(status_code=404, detail="Request not found")
    pending_requests[request_id]["status"] = "blacklisted"
    return {"message": "Visitor blacklisted", "request_id": request_id}

@app.get("/status/{request_id}")
def get_status(request_id: str):
    if request_id not in pending_requests:
        raise HTTPException(status_code=404, detail="Request not found")
    return pending_requests[request_id]

# New endpoint to get all pending requests
@app.get("/status/all")
def get_all_status():
    return pending_requests

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)