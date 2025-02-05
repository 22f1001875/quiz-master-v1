import os
from flask import Flask
from models.models import db

app = None


def start_app():
    app=Flask(__name__,template_folder="templates")
    app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///quizmasterdb.sqlite3"
    db.init_app(app)
    app.app_context().push()
    app.debug = True
    return app


app=start_app()

from controllers.controllers import *

if __name__=="__main__":
    app.run()