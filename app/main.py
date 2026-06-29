from datetime import datetime
from typing import Literal

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

ApplicationStatus = Literal["Pending", "Approved", "Rejected"]


class ApplicationResponse(BaseModel):
    id: int
    title: str
    content: str
    status: ApplicationStatus
    created_at: datetime

class CreateApplicationRequest(BaseModel):
    title: str
    content: str

applications: list[ApplicationResponse] = [
    ApplicationResponse(
        id=1,
        title="出張申請",
        content="東京への出張申請です。",
        status="Pending",
        created_at=datetime.now(),
    ),
    ApplicationResponse(
        id=2,
        title="備品購入申請",
        content="キーボード購入の申請です。",
        status="Approved",
        created_at=datetime.now(),
    ),
]

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/applications", response_model=list[ApplicationResponse])
def get_applications():
    return applications

@app.get("/applications/{application_id}", response_model=ApplicationResponse)
def get_application_by_id(application_id: int):
    for application in applications:
        if application.id == application_id:
            return application
    
    raise HTTPException(status_code=404, detail="Application not found")

@app.post("/applications", response_model=ApplicationResponse, status_code=201)
def create_application(request: CreateApplicationRequest):
    new_id = max(application.id for application in applications) + 1

    application = ApplicationResponse(
        id=new_id,
        title=request.title,
        content=request.content,
        status="Pending",
        created_at=datetime.now(),
    )

    applications.append(application)
    
    return application