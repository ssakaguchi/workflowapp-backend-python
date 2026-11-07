from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict

ApplicationStatus = Literal["Pending", "Approved", "Rejected"]


class ApplicationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    content: str
    status: ApplicationStatus
    created_at: datetime


class CreateApplicationRequest(BaseModel):
    title: str
    content: str


