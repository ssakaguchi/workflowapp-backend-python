from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.repository.application import ApplicationRepository


def get_application_repository(
    db: Annotated[Session, Depends(get_db)],
) -> ApplicationRepository:
    """
    FastAPIから注入されたDBセッションを使ってRepositoryを生成する
    Arguments:
        db: FastAPIの依存注入で渡されるデータベースセッション
    Returns:
        ApplicationRepository: 生成した申請Repository
    Raises:
        なし
    """
    return ApplicationRepository(db)
