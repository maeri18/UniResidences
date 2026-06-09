from models import db
from sqlalchemy.orm import Mapped
from typing import List


class Admin(db.Model):
    __tablename__ = "admins"

    admin_Id = db.Column(db.Integer, primary_key=True)
    password_hash = db.Column(db.String(100), nullable=False)
    handled: Mapped[List["Application"]] = db.relationship(back_populates="handledBy")

    def to_dict(self):
        return {
            "id": self.admin_Id,
            "handled": [application.application_Id for application in self.handled],
        }
