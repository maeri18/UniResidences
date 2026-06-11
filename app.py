from flask import Flask
from flask_cors import CORS
from sqlalchemy import URL

import random
import string
import hashlib

from models import db

# import all models
from models.Student import Student, generate_random_student_id
from models.Room import Room, generate_random_room_id
from models.Admin import Admin, generate_random_admin_id

# import routes
from routes.student_routes import student_bp
from routes.admin_routes import admin_bp

from dotenv import load_dotenv
import os

load_dotenv()

def create_uniResidences_app():

    app = Flask(__name__)
    CORS(app, supports_credentials=True, origins=["http://localhost:5173"])

    databaseUserName = os.environ.get("DATABASE_USERNAME")
    databasePassword = os.environ.get("DATABASE_PASSWORD")
    databaseName = os.environ.get("DATABASE_NAME")
    databaseURL = URL.create("postgresql", username=databaseUserName, password=databasePassword, host="localhost", port=5432, database=databaseName)
    app.config["SQLALCHEMY_DATABASE_URI"] = databaseURL
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "defaultKey")

    db.init_app(app)

    app.register_blueprint(student_bp, url_prefix="/student")
    app.register_blueprint(admin_bp,  url_prefix="/admin")

    with app.app_context():
        db.create_all()

    return app







if __name__ == "__main__":
    uniResidences_app = create_uniResidences_app()
    uniResidences_app.run()