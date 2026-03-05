import click

from wiki import db
from wiki.core.models.authentication import User

from . import cli


@cli.cli.command("create-user")
def create_user():
    username = click.prompt("Username")
    password = click.prompt(
        "Password (leave blank to create inactive user)", hide_input=True, default=""
    )
    email = click.prompt("Email address (optional)", default="")

    new_user = User(username=username, source="cli")

    if email != "":
        new_user.email = email

    if password != "":
        new_user.set_password(password)
        new_user.active = True

    db.session.add(new_user)
    db.session.commit()
