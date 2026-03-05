from flask_login import LoginManager

from wiki.core.database import db
from wiki.core.models.authentication import User

login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id: str) -> User:
    query = db.select(User).where(User.username == user_id).limit(1)
    return db.session.scalars(query)[0]
