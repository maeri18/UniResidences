from models import db
import enum
from sqlalchemy.orm import Mapped
from typing import List
import random

def generate_random_room_id():
    return random.randint(100,10000)

class Room(db.Model):
    __tablename__ = "rooms"

    room_Id = db.Column(db.Integer, primary_key=True,autoincrement=False, default=generate_random_room_id)
    available = db.Column(db.Boolean, nullable=False)
    rent = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(300), nullable=False)

    isLinkedTo: Mapped[List["Application"]] = db.relationship(back_populates="linksTo")

    def to_dict(self):
        return {
            "id": self.room_Id,
            "available": self.available,
            "rent": self.rent,
            "description": self.description,
            "applications": [
                application.application_Id for application in self.isLinkedTo
            ],
        }

    def getRoomID(self) -> int:
        return self.room_Id

    def getRoomDescription(self) -> str:
        return self.description

    def getRoomRent(self) -> int:
        return self.rent

    def getRoomAvailability(self) -> bool:
        return self.available
