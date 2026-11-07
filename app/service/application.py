from fastapi import HTTPException

from app.models.application import Application
from app.repository.application import ApplicationRepository


class ApplicationService:
    def __init__(self, repository: ApplicationRepository):
        """
        申請のDBアクセスに使うRepositoryを受け取る
        Arguments:
            repository: 申請のDBアクセスを担当するRepository
        Returns:
            None
        Raises:
            なし
        """
        self.repository = repository

    def get_applications(self) -> list[Application]:
        """
        Repositoryからすべての申請を取得する
        Arguments:
            なし
        Returns:
            list[Application]: 取得した申請のリスト
        Raises:
            SQLAlchemyError: DBアクセス時にSQLAlchemyのエラーが発生した場合
        """
        return self.repository.find_all()

    def get_application_by_id(self, application_id: int) -> Application:
        """
        指定IDの申請を取得する
        Arguments:
            application_id: 取得する申請のID
        Returns:
            Application: 取得した申請
        Raises:
            HTTPException: 指定IDの申請が見つからない場合（404）
            SQLAlchemyError: DBアクセス時にSQLAlchemyのエラーが発生した場合
        """
        application = self.repository.find_by_id(application_id)

        if application is None:
            raise HTTPException(
                status_code=404,
                detail="Application not found",
            )

        return application
