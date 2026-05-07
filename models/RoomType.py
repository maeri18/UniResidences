from models import db
import enum


class RoomTypeEnum(enum.Enum):
    TYPE_1 = "Type 1: Single room. Shared bathroom and kitchen, average size: 15 m2"
    TYPE_2 = (
        "Type 2: Single room. Private bathroom, shared kitchen, average surface: 19 m2"
    )
    TYPE_3 = "Type 3: Studio apartment. Private bathroom and kitchen. Single, average size, 24 m2"
    TYPE_4 = "Type 4: Studio apartment. Private bathroom and kitchen. Double (only for couples), average size, 35 m2"
    TYPE_5 = "Type 5: Two-room apartment. Private kitchen/living room, bathroom and one bedroom. (Only for couples): average size, 44 m2"


class RoomType(db.Model):
    __tablename__ = "roomTypes"

    room_type = db.Column(db.Enum(RoomTypeEnum), primary_key=True)
    current_availability = db.Column(db.Integer, nullable=False)
    total_availability = db.Column(db.Integer, nullable=False)
