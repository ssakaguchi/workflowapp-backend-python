from datetime import datetime
from typing import Annotated, Literal

from fastapi import Depends, FastAPI
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.application import Application
from app.service import get_application_service
from app.service.application import ApplicationService

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
def get_applications(
    service: Annotated[
        ApplicationService,
        Depends(get_application_service),
    ],
):
    """
    Serviceを通じてすべての申請を取得する
    Arguments:
        service: 申請取得処理を担当するService
    Returns:
        list[Application]: レスポンスの元になる申請のリスト
    Raises:
        SQLAlchemyError: DBアクセス時にSQLAlchemyのエラーが発生した場合
    """
    return service.get_applications()


@app.get("/applications/{application_id}", response_model=ApplicationResponse)
def get_application_by_id(
    application_id: int,
    service: Annotated[
        ApplicationService,
        Depends(get_application_service),
    ],
):
    """
    指定IDの申請をServiceから取得する
    Arguments:
        application_id: 取得する申請のID
        service: 申請取得処理を担当するService
    Returns:
        Application: レスポンスの元になる申請
    Raises:
        HTTPException: 指定IDの申請が見つからない場合（404）
        SQLAlchemyError: DBアクセス時にSQLAlchemyのエラーが発生した場合
    """
    return service.get_application_by_id(application_id)


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
