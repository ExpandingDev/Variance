from datetime import datetime

import click
from flask.cli import AppGroup

from variance import db
from variance.models.user import UserModel

user_cli = AppGroup("user")
user_mod_cli = AppGroup("mod")
user_cli.add_command(user_mod_cli)

@user_cli.command("get")
@click.argument("username")
def cli_user_add(username):
    u = UserModel.query.filter_by(username=username).first()
    if u is None:
        click.echo("No user with that username found!")
        return -1
    click.echo("User ID: " + str(u.id))

@user_cli.command("add")
@click.argument("username")
@click.argument("password")
@click.argument("birthdate")
def cli_user_add(username, password, birthdate):
    u = UserModel.query.filter_by(username=username).first()
    if u is not None:
        click.echo("A user with that username already exists!")
        return -1
    try:
        birthdate = datetime.fromisoformat(birthdate)
    except ValueError:
        click.echo("Birthdate must be in YYYY-MM-DD format!")
        return -1
    new_user = UserModel(username=username, birthdate=birthdate)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()
    click.echo("User added.")

@user_cli.command("del")
@click.argument("user_id")
def cli_user_del(user_id):
    u = UserModel.query.get(user_id)
    if u is None:
        click.echo("No user with that ID found!")
        return -1
    db.session.delete(u)
    db.session.commit()
    click.echo("User deleted.")