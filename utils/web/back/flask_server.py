from flask import Flask

# Additional options: --host=0.0.0.0
app = Flask(__name__)


@app.route('/')
def index():
    return 'Hello, world!'


@app.route('/search/q=<string:question>')
def search(question):
    return 'Question: %s' % question
