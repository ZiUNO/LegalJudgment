import json

from flask import Flask, render_template, request
from werkzeug.exceptions import HTTPException

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template("index.html")


@app.route('/search')
def search():
    q = request.args.get('q')
    return q


@app.errorhandler(HTTPException)
def handle_exception(e):
    exception = {
        "code": e.code,
        "name": e.name,
        "description": e.description,
    }
    return render_template("exception.html", exception=exception)
