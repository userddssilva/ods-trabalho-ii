from flask import Flask, render_template
from flask import redirect, url_for, request
from .backend.connection import Connection
from .backend import recommender

app = Flask(__name__)

connection = Connection()
connection.populate_animes()

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
        return render_template("home.html")
    else:
        return render_template("login.html")


@app.route("/first_login/<user_id>")
def first_login(user_id=None):
    print(f"##=user_id={user_id}")
    # recommendations = connection.get_json()
    recommendations = connection.get_n_animes()
    print(f"##=recomendations={recommendations}")
    return render_template("first-login.html", recommends=recommendations)

@app.route("/sign_up")
def sign_up():
    print(connection.get_all_animes())
    return render_template("sign-up.html")


@app.route("/create_user", methods=["POST"])
def create_user():
    connection.createUser(request.form["email"], request.form["password"])
    return render_template("login.html")


@app.route("/home")
def home(recommended_animes):
    pass

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
