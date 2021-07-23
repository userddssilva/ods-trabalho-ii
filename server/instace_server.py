from flask import Flask

app = Flask(__name__)


@app.route("/teste")
def index():
    return 'Olá Mundo!'


def init_connection():
    app.run()
