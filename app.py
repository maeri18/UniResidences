from flask import Flask
from flask_cors import CORS

from models import db

# import all models
from models.Student import Student
from models.Application import Application
from models.Contract import Contract
from models.Room import Room
from models.Residence import Residence

from models.Admin import Admin

from dotenv import load_dotenv
import os

load_dotenv()


app = Flask(__name__)
CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")

db.init_app(app)

# register blueprints here


with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
