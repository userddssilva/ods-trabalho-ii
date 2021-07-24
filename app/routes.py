from flask import Flask, render_template, request
from backend.connection import Connection
import backend.recommender as recommender

app = Flask(__name__)

connection = Connection()


@app.route("/")
def index():
    return render_template("login.html")


@app.route("/sign_up")
def sign_up():
    return render_template("sing-up.html")


@app.route("/create_user", methods=["POST"])
def create_user():
    connection.createUser(request.form["email"], request.form["password"])
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def test():
    login = request.form["email"]
    password = request.form["password"]
    if connection.get_user(login, password) is not None:
        return render_template("home.html")


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
