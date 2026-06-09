from flask import Flask
from flask_cors import CORS

import random
import string
import hashlib

from models import db

# import all models
from models.Student import Student
from models.Application import Application
from models.Room import Room
from models.Admin import Admin

# import routes
from routes.student_routes import student_bp, start_logging
from routes.admin_routes import admin_bp

from dotenv import load_dotenv
import os

load_dotenv()

start_logging()


app = Flask(__name__)
CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")

db.init_app(app)


## For manual testing ##
def initDatabase():

    roomDescriptions = {
        1: "Type 1: Single room. Shared bathroom and kitchen, average size: 15 m2",
        2: "Type 2: Single room. Private bathroom, shared kitchen, average surface: 19 m2",
        3: "Type 3: Studio apartment. Private bathroom and kitchen. Single, average size, 24 m2",
        4: "Type 4: Studio apartment. Private bathroom and kitchen. Double (only for couples), average size, 35 m2",
        5: "Type 5: Two-room apartment. Private kitchen/living room, bathroom and one bedroom. (Only for couples): average size, 44 m2",
    }

    location = {
        1: "Esch-sur-Alzette",
        2: "Niederkorn",
        3: "Luxembourg City",
        4: "Kayl",
        5: "Dudelange",
        6: "Differdange",
        7: "Clervaux",
        8: "Ettelbruck",
        9: "Mersch",
    }

    random.seed(10)

    for i in range(10):
        room = Room(
            available=True,
            rent=random.randint(350, 750),
            description=roomDescriptions[random.randint(1, 5)]
            + ". Located at : "
            + location[random.randint(1, 9)],
        )
        db.session.add(room)

    for i in range(5):
        student_name = "".join(
            random.choices(string.ascii_letters, k=random.randint(5, 10))
        )
        password = "".join(
            random.choices(
                string.ascii_letters + string.digits + string.punctuation,
                k=random.randint(6, 12),
            )
        )
        student = Student(
            student_name=student_name,
            password_hash=hashlib.shake_256(password.encode("utf-8")).hexdigest(50),
        )

        db.session.add(student)

    for i in range(2):
        password = "".join(
            random.choices(
                string.ascii_letters + string.digits + string.punctuation,
                k=random.randint(12, 15),
            )
        )
        admin = Admin(
            password_hash=hashlib.shake_256(password.encode("utf-8")).hexdigest(50),
        )

        db.session.add(admin)

    db.session.commit()


app.register_blueprint(student_bp)
app.register_blueprint(admin_bp)

with app.app_context():
    db.drop_all()
    db.create_all()
    initDatabase()


if __name__ == "__main__":
    app.run()
