# this file will create the website_code directory into a python package.

from flask import Flask

from .database import db
from .models import *

from flask_login import LoginManager


def make_app():     # we are making our flask app.
    app=Flask(__name__)
    app.config["SECRET_KEY"] = "This is a secret ket" # this secret key is used to encrypt session and cookies data related to website.
    #initialize database
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.sqlite3"
    db.init_app(app)

    from .views import views  # first views is the file name (it has to start with dot) and second views is the variable name in views.py
    from .authentication import auth  # this make it more clear. compare it with views.

    # register the Blueprint to the app.
    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")


    login_mngr=LoginManager()
    login_mngr.login_view = 'auth.login'
    login_mngr.init_app(app)

    @login_mngr.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app