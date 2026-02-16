from datetime import datetime, timedelta
from uuid import uuid4

from werkzeug.exceptions import abort

from flask import session, request
from passlib.hash import argon2
from database import read_query, insert, update


def get_user(user_id: int):
    user = read_query("SELECT * FROM users WHERE id = ?", (user_id,), one=True)
    return user


def create_user(username, email=None, password=None):
    values = {"username": username}

    if email is not None:
        values["email_address"] = email

    if password is not None:
        values["password_hash"] = hash_password(password)

    insert("users", values)


def update_user(user_id: int, email=None, password=None, page_title=None):
    values = {}

    if email is not None:
        values["email_address"] = email

    if password is not None:
        values["password_hash"] = hash_password(password)

    if page_title is not None:
        values["page_title"] = page_title

    update("users", {"id": user_id}, values)


def activate_user(user_id: int, set_active: bool = True):
    update("users", {"id": user_id}, {"set_active": set_active})


def check_credentials(username, password):
    user = read_query("SELECT * FROM users WHERE username = ?", (username,), one=True)
    if user is None:
        return False

    if user["password_hash"] is None or not argon2.verify(
        password, user["password_hash"]
    ):
        return False

    return True


def login_user(user_id, remember: bool = False):
    # Create a session
    new_id = uuid4().hex
    new_session = {
        "id": new_id,
        "user_id": user_id,
        "ip_address": request.remote_addr,
        "remember_me": remember,
        "user_agent": request.headers.get("User-Agent"),
        "expires_at": datetime.now() + timedelta(days=8),
        "last_activity_at": datetime.now(),
    }

    insert("sessions", new_session)
    session["session_id"] = new_id


def logout_current_user():
    session.pop("session_id", None)


def hash_password(raw_password):
    return argon2.hash(raw_password)


def get_current_user(gate=False):
    if "session_id" not in session:
        if gate:
            raise abort(401)
        else:
            return None

    session_id = session["session_id"]
    db_session = read_query(
        "SELECT * FROM sessions WHERE id = ?", (session_id,), one=True
    )
    user = get_user(db_session["user_id"])

    if gate and user is None:
        raise abort(401)

    return user
