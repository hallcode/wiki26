from flask_alembic import Alembic
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase


class Model(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Model)
alembic = Alembic()
