from flask import Flask
from flask_cors import CORS
from sqlalchemy import URL

import random
import string
import hashlib

from models import db

# import all models
from models.Student import Student
from models.Room import Room
from models.Admin import Admin

# import routes
from routes.student_routes import student_bp
from routes.admin_routes import admin_bp

from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
CORS(app, supports_credentials=True)

databaseUserName = os.environ.get("DATABASE_USERNAME")
databasePassword = os.environ.get("DATABASE_PASSWORD")
databaseURL = URL.create("postgresql", username=databaseUserName, password=databasePassword, host="localhost", port=5432, database="uniResidences")
app.config["SQLALCHEMY_DATABASE_URI"] = databaseURL
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "defaultKey")


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

    print_one = True

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

        if print_one:
            print("A student is: ", student_name, "and password: ", password)
            print_one = False
        
        student = Student(
            student_name=student_name,
            password_hash=hashlib.shake_256(password.encode("utf-8")).hexdigest(50),
        )

        db.session.add(student)

    print_one = True
    for i in range(2):
        password = "".join(
            random.choices(
                string.ascii_letters + string.digits + string.punctuation,
                k=random.randint(12, 15),
            )
        )

        if print_one:
            print("An admin password: ", password)
            print_one = False
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
    app.run(debug=True)
