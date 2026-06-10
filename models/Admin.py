from models import db
from sqlalchemy.orm import Mapped
from typing import List
import random

def generate_random_admin_id():
    return random.randint(100,10000)

class Admin(db.Model):
    __tablename__ = "admins"

    admin_Id = db.Column(db.Integer, primary_key=True, autoincrement=False, default=generate_random_admin_id)
    password_hash = db.Column(db.String(120), nullable=False)
    handled: Mapped[List["Application"]] = db.relationship(back_populates="handledBy")

    def to_dict(self):
        return {
            "id": self.admin_Id,
            "handled": [application.application_Id for application in self.handled],
        }
