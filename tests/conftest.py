import pytest
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



def initDatabase(session):
    random.seed(42)

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


    for i in range(5):
        rent = random.randint(350, 750)
        room_id = generate_random_room_id()
        while session.get(Room, room_id) is not None:
            room_id = generate_random_room_id()

        room = Room(
            room_Id=room_id,
            available=True,
            rent=rent,
            description=roomDescriptions[random.randint(1, 5)]
            + ". Located at : "
            + location[random.randint(1, 9)] + f"\nRent: {rent}",
        )
        session.add(room)

    for i in range(3):
        student_name = "".join(
            random.choices(string.ascii_letters, k=random.randint(5, 10))
        )
        password = "".join(
            random.choices(
                string.ascii_letters + string.digits + string.punctuation,
                k=random.randint(6, 12),
            )
        )

        student_id = generate_random_student_id()
        while session.get(Student, student_id) is not None:
            student_id = generate_random_student_id()

        
        student = Student(
            student_Id=student_id,
            student_name=student_name,
            password_hash=hashlib.shake_256(password.encode("utf-8")).hexdigest(50),
        )

        session.add(student)

    for i in range(2):
        password = "".join(
            random.choices(
                string.ascii_letters + string.digits + string.punctuation,
                k=random.randint(12, 15),
            )
        )

        admin_id = generate_random_admin_id()
        while session.get(Admin, admin_id) is not None:
            admin_id = generate_random_admin_id()


        admin = Admin(
            admin_Id=admin_id,
            password_hash=hashlib.shake_256(password.encode("utf-8")).hexdigest(50),
        )

        session.add(admin)

    session.commit()

@pytest.fixture(scope="session")
def create_app():
    """This fixture creates a Flask application instance for testing purposes.
      It configures the application to use a test database and registers the necessary blueprints for handling student and admin routes."""

    app = Flask(__name__)
    CORS(app, supports_credentials=True, origins=["http://localhost:5173"])

    databaseUserName = os.environ.get("DATABASE_USERNAME")
    databasePassword = os.environ.get("DATABASE_PASSWORD")
    databaseName = os.environ.get("TEST_DATABASE_NAME")
    databaseURL = URL.create("postgresql", username=databaseUserName, password=databasePassword, host="localhost", port=5432, database=databaseName)
    app.config["SQLALCHEMY_DATABASE_URI"] = databaseURL
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "defaultKey")

    db.init_app(app)

    app.register_blueprint(student_bp, url_prefix="/student")
    app.register_blueprint(admin_bp,  url_prefix="/admin")

    return app


@pytest.fixture(scope="function")
def new_db(create_app):
    """ This fixture sets up a new database session for each test function. 
    It drops all existing tables, creates new ones, and initializes the database with sample data using the `initDatabase` function. 
    After the test function is executed, it removes the database session to ensure a clean state for the next test."""
    with create_app.app_context():
        db.drop_all()
        db.create_all()
        initDatabase(db.session)

        yield db.session

        db.session.remove()



@pytest.fixture(scope="function")
def new_client(create_app,new_db):
    """ This fixture provides a test client for the Flask application. 
    """

    return create_app.test_client(use_cookies=True)




