import click
from flask.cli import with_appcontext

from . import db


@click.command(name='create_tables')
@with_appcontext
def create_tables():
    from penfriend.models import User, Message
    db.create_all()
