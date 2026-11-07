from typing import Annotated

from fastapi import Depends

from app.repository import get_application_repository
from app.repository.application import ApplicationRepository
from app.service.application import ApplicationService


def get_application_service(
    repository: Annotated[
        ApplicationRepository,
        Depends(get_application_repository),
    ],
) -> ApplicationService:
    """
    FastAPIから注入されたRepositoryを使ってServiceを生成する
    Arguments:
        repository: FastAPIの依存注入で渡される申請Repository
    Returns:
        ApplicationService: 生成した申請Service
    Raises:
        なし
    """
    return ApplicationService(repository)
