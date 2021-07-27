from abc import abstractproperty
import enum
import itertools
import re
from flask import Flask, render_template, jsonify
from flask import redirect, url_for, request
from flask.ctx import after_this_request
from .backend.connection import Connection
from .backend.recommender import computeNearestNeighbor

app = Flask(__name__)

connection = Connection()
connection.populate_animes()
login = ''
password = ''

@app.route("/")
def index():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login():
    login = request.form["email"]
    password = request.form["password"]
    user = connection.get_user(login, password)
    if user is not None:
        animes = connection.get_animes_user(user['id'])
        if len(animes) <= 0:
            return redirect(url_for('first_login', user_id=user['id']))
        return redirect(url_for('hub', user_id=user['id']))
    else:
        return redirect(url_for('hub', user_id=user['id']))


@app.route("/first_login/<user_id>")
def first_login(user_id=None):
    print(f"##=user_id={user_id}")
    recommendations = connection.get_n_animes(n=50)
    print(f"##=recomendations={recommendations}")
    return render_template(
        "first-login.html", 
        recommends=recommendations, enumerate=enumerate,
        user_id=user_id
    )


@app.route("/sign_up")
def sign_up():
    print(connection.get_all_animes())
    return render_template("sign-up.html")


@app.route("/create_user", methods=["POST"])
def create_user():
    connection.createUser(request.form["email"], request.form["password"])
    return render_template("login.html")


@app.route("/hub/<user_id>", methods=['POST', 'GET'])
def hub(user_id=None):
    if request.method == "POST":
        # user_id = request.form['user_id']
        animes = request.form['animes']
        for anime_id in animes.split(','):
            connection.rate_anime(anime_id, user_id, 3)
        return user_id
    else:
        return redirect(url_for('home', user_id=user_id))


@app.route("/home/<user_id>")
def home(user_id):
    # Rated animes 
    animes_rated = connection.get_animes_user(id_user=user_id)
    animes_rated_id = [x for x,_ in animes_rated]
    recommend_animes = []
    for anime_id in animes_rated_id:
        neighbors = computeNearestNeighbor(anime_id)
        recommend_animes.append(neighbors)
    
    # Recommend animes
    recommend_animes = list(itertools.chain(*recommend_animes))
    recommend_animes.sort()
    recommend_animes = [anime_id for _, anime_id in recommend_animes]
    recommends = connection.get_animes(recommend_animes)

    # Avegare rate animes
    averages_rate_animes = []
    for anime in recommend_animes:
        avg = connection.average_rate_anime(anime)
        averages_rate_animes.append(avg)

    return render_template(
        "home.html", 
        enumerate=enumerate,
        recommends=recommends,
        averages=averages_rate_animes
    )


@app.route("/details/<anime_id>",  methods=['GET'])
def details(anime_id):
    anime = connection.get_anime(anime_id)
    average_rate = connection.average_rate_anime(anime_id)

    return render_template(
        "detalhe.html",
        anime=anime,
        average_rate=average_rate
    )


@app.route("/avalia/<anime_id>", methods=["GET"])
def avalia(anime_id):
    anime = connection.get_anime(anime_id)
    user = connection.get_user(login, password)
    print(user)
    return render_template(
        "avalia.html",
        anime=anime,
        user=user
    )

@app.route("/rate_anime/<iduser>/<anime>/<rate>", strict_slashes=False)
def rate_anime(iduser, anime, rate):
    try:
        connection.rate_anime(anime, iduser, rate)
        return "Anime avaliado com sucesso"
    except:
        return "Ocorreu um erro durante a avalição tente novamente"


@app.route("/recommend/<anime>", strict_slashes=False)
def recommend(anime):
    return computeNearestNeighbor(anime)
