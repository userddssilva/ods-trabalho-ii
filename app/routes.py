import re
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
    # return str(connection.get_animes_user(id_user=user_id))
    # return str(connection.get_animes(['a612c40a-497c-40b9-99a1-e26447fd7baa', 'c11b7e25-7907-495f-a56a-e0dd3915a4ba', '5505a9f0-7e7f-482d-83fb-37bd057bd273', '0227de08-c4ba-49bc-9b6b-baedbeeb740f']))
    # return render_template("home.html")
    # return str(connection.get_anime('a612c40a-497c-40b9-99a1-e26447fd7baa'))
    return str(connection.get_all_animes_json())


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
