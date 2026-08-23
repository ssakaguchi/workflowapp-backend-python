from datetime import datetime
from typing import Annotated, Literal

from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel, ConfigDict
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.base import Base
from app.db.database import engine, get_db
from app.models.application import Application

Base.metadata.create_all(bind=engine)

app = FastAPI()

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


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/applications", response_model=list[ApplicationResponse])
def get_applications(db: Annotated[Session, Depends(get_db)]):
    """
    すべての申請を取得する
    Arguments:
        db: データベースセッション
    Returns:
        list[Application]: 取得した申請のリスト
    Raises:
        HTTPException: データベースエラーが発生した場合
    """
    statement = select(Application).order_by(Application.id)
    applications = db.scalars(statement).all()

    return applications


@app.get("/applications/{application_id}", response_model=ApplicationResponse)
def get_application_by_id(application_id: int, db: Annotated[Session, Depends(get_db)]):
    """
    申請IDに基づいて申請を取得する

    Arguments:
        application_id: 申請ID
    Returns:
        Application: 取得した申請
    Raises:
        HTTPException: 申請が見つからない場合
    """

    application = db.get(Application, application_id)

    if application is None:
        raise HTTPException(status_code=404, detail="Application not found")

    return application


@app.post("/applications", response_model=ApplicationResponse, status_code=201)
def create_application(
    request: CreateApplicationRequest, db: Annotated[Session, Depends(get_db)]
):

    application = Application(
        title=request.title,
        content=request.content,
        status="Pending",
        created_at=datetime.now(),
    )

    db.add(application)
    db.commit()
    db.refresh(application)

    return application
