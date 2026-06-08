from models import db
import enum
from sqlalchemy.orm import Mapped
from typing import List


class RoomTypeEnum(enum.Enum):
    TYPE_1 = "Type 1: Single room. Shared bathroom and kitchen, average size: 15 m2"
    TYPE_2 = (
        "Type 2: Single room. Private bathroom, shared kitchen, average surface: 19 m2"
    )
    TYPE_3 = "Type 3: Studio apartment. Private bathroom and kitchen. Single, average size, 24 m2"
    TYPE_4 = "Type 4: Studio apartment. Private bathroom and kitchen. Double (only for couples), average size, 35 m2"
    TYPE_5 = "Type 5: Two-room apartment. Private kitchen/living room, bathroom and one bedroom. (Only for couples): average size, 44 m2"


class Room(db.Model):
    __tablename__ = "rooms"

    room_Id = db.Column(db.Integer, primary_key=True)
    availability = db.Column(db.Boolean, nullable=False)
    rent = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(300), nullable=False)

    isLinkedTo: Mapped[List["Application"]] = db.relationship(back_populates="linksTo")

    def to_dict(self):
        return {
            "id": self.room_Id,
            "availability": self.availability,
            "rent": self.rent,
            "description": self.description,
            "applications": [
                application.application_Id for application in self.isLinkedTo
            ],
        }
