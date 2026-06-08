from flask import Flask
from flask_cors import CORS

from models import db

# import all models
from models.Student import Student
from models.Application import Application
from models.Room import Room
from models.Admin import Admin

# import routes
from routes.student_routes import student_bp
from routes.admin_routes import admin_bp

from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")

db.init_app(app)

# register blueprints here
app.register_blueprint(student_bp)
app.register_blueprint(admin_bp)

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
