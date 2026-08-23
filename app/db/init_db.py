from app.db.base import Base
from app.db.database import engine
from app.models.application import Application  # noqa: F401


def init_db():
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    init_db()
