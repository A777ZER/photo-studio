from back.app.db.base import Base
from back.app.db.session import engine
from back.app import models


def init_db() -> None:
    Base.metadata.create_all(bind=engine)
