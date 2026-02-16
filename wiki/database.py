import sqlite3
from typing import Any

from flask import g

DATABASE = "../data/wiki.sqlite"


def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


def close_db(app):
    @app.teardown_appcontext
    def close_connection(exception):
        db = getattr(g, "_database", None)
        db.row_factory = sqlite3.Row
        if db is not None:
            db.close()


def read_query(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()

    if len(rv) == 1:
        return rv[0]

    return rv


def non_read_query(query, args=()):
    db = get_db()
    cur = db.execute(query, args)
    db.commit()
    cur.close()


def insert(table, values: dict[str, Any], return_row=False):
    columns = ", ".join(values.keys())
    placeholders = ", ".join(["?"] * len(values))
    query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
    non_read_query(query, list(values.values()))

    if return_row:
        return read_query(f"SELECT * from {table} where ROWID = last_insert_rowid()")
    return None


def update(table, primary_keys: dict[str, Any], values: dict[str, Any]):
    pks = ""
    for key, value in primary_keys.items():
        pks += f" {key} = ?"

    terms = ""
    for key, value in values.items():
        terms += f" {key} = ?"

    query = f"UPDATE {table} SET {terms} WHERE {pks}"
    args = list(values.values()) + list(primary_keys.values())
    non_read_query(query, args)
