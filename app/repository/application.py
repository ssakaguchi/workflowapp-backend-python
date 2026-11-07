from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.application import Application


class ApplicationRepository:
    def __init__(self, db: Session):
        """
        申請のDBアクセスに使うセッションを受け取る
        Arguments:
            db: データベースセッション
        Returns:
            None
        Raises:
            なし
        """
        self.db = db

    def find_all(self) -> list[Application]:
        """
        すべての申請をIDの昇順でDBから取得する
        Arguments:
            なし
        Returns:
            list[Application]: 取得した申請のリスト
        Raises:
            SQLAlchemyError: DBアクセス時にSQLAlchemyのエラーが発生した場合
        """
        statement = select(Application).order_by(Application.id)
        return list(self.db.scalars(statement).all())

    def find_by_id(self, application_id: int) -> Application | None:
        """
        指定IDの申請をDBから取得する
        Arguments:
            application_id: 取得する申請のID
        Returns:
            Application | None: 取得した申請。見つからない場合はNone
        Raises:
            SQLAlchemyError: DBアクセス時にSQLAlchemyのエラーが発生した場合
        """
        return self.db.get(Application, application_id)
