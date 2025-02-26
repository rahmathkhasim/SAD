from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict
import uvicorn
import json
import os

app = FastAPI()

# File-based storage for pending requests
STORAGE_FILE = "pending_requests.json"

def load_requests() -> Dict[str, dict]:
    if os.path.exists(STORAGE_FILE):
        with open(STORAGE_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_requests(requests: Dict[str, dict]):
    with open(STORAGE_FILE, 'w') as f:
        json.dump(requests, f)

class ApprovalRequest(BaseModel):
    visitor_name: str
    visitor_phone: str
    resident_email: str
    status: str = "pending"

@app.post("/request/{request_id}")
def create_request(request_id: str, request: ApprovalRequest):
    requests = load_requests()
    requests[request_id] = request.dict()
    save_requests(requests)
    return {"message": "Request created", "request_id": request_id}

# Allow both GET and POST for approve/deny/blacklist
@app.post("/approve/{request_id}")
@app.get("/approve/{request_id}")
def approve_request(request_id: str):
    requests = load_requests()
    if request_id not in requests:
        raise HTTPException(status_code=404, detail="Request not found")
    requests[request_id]["status"] = "approved"
    save_requests(requests)
    return {"message": "Request approved", "request_id": request_id}

@app.post("/deny/{request_id}")
@app.get("/deny/{request_id}")
def deny_request(request_id: str):
    requests = load_requests()
    if request_id not in requests:
        raise HTTPException(status_code=404, detail="Request not found")
    requests[request_id]["status"] = "denied"
    save_requests(requests)
    return {"message": "Request denied", "request_id": request_id}

@app.post("/blacklist/{request_id}")
@app.get("/blacklist/{request_id}")
def blacklist_request(request_id: str):
    requests = load_requests()
    if request_id not in requests:
        raise HTTPException(status_code=404, detail="Request not found")
    requests[request_id]["status"] = "blacklisted"
    save_requests(requests)
    return {"message": "Visitor blacklisted", "request_id": request_id}

@app.get("/status/{request_id}")
def get_status(request_id: str):
    requests = load_requests()
    if request_id not in requests:
        raise HTTPException(status_code=404, detail="Request not found")
    return requests[request_id]

@app.get("/status/all")
def get_all_status():
    return load_requests()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
