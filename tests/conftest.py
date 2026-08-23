from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.base import Base
from app.db.database import get_db
from app.main import app

TEST_DATABASE_URL = "sqlite://"

test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine,
)


def override_get_db() -> Generator[Session, None, None]:
    """
    テスト用のデータベースセッションを取得するための依存関係をオーバーライドする関数

    Arguments:
        None
    Returns:
        Generator[Session, None, None]: テスト用のデータベースセッション
    Raises:
        None
    """

    db = TestSessionLocal()

    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client() -> Generator[TestClient, None, None]:
    """
    FastAPIのテストクライアントを提供するpytestのフィクスチャ

    Arguments:
        None
    Returns:
        Generator[TestClient, None, None]: FastAPIのテストクライアント
    Raises:
        None

    """
    Base.metadata.create_all(bind=test_engine)

    # テスト用のデータベースセッションを使用するように依存関係をオーバーライド
    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=test_engine)
