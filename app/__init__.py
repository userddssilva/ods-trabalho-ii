# export FLASK_APP=flaskr
# export FLASK_ENV=development
# flask run

from .routes import app

if __name__ == "__main__":
	app.run()