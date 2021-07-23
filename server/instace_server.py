from flask import Flask
from backend.connection import Connection
import backend.recommender as recommender

app = Flask(__name__)

connection = Connection()


@app.route("/create_user/<login>/<password>", strict_slashes=False)
def create_user(login, password):
    return connection.createUser(login, password)


@app.route("/rate_anime/<iduser>/<anime>/<rate>", strict_slashes=False)
def rate_anime(iduser, anime, rate):
    try:
        connection.rate_anime(anime, iduser, rate)
        return "Anime avaliado com sucesso"
    except:
        return "Ocorreu um erro durante a avalição tente novamente"


@app.route("/recommend/<anime>", strict_slashes=False)
def recommend(anime):
    return recommender.computeNearestNeighbor(anime)


def init_connection():
    app.run()
