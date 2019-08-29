#!/usr/bin/env python
from flask_script import Manager
from sqlalchemy_utils.functions import database_exists, create_database
from application import app, db

manager = Manager(app)


def do_init_db():
    if not database_exists(db.engine.url):
        create_database(db.engine.url)
    db.create_all()


def do_reset_db():
    db.drop_all()
    do_init_db()


@manager.command
def initdb():
    do_init_db()
    print("Database initialized.")


@manager.command
def resetdb():
    do_reset_db()
    print("Database dropped and reinitialized.")


@manager.shell
def make_shell_context():
    return dict(app=app, db=db)


if __name__ == "__main__":
    manager.run()
