import py2neo

import click
from flask import current_app, g
from flask.cli import with_appcontext

def get_db():
    if 'db' not in g:
        g.db = py2neo.Graph('http://localhost:7474', username='ziuno', password='1234').database

    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

