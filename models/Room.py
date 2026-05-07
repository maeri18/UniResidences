from models import db
from models.RoomType import RoomTypeEnum


class Room(db.Model):
    __tablename__ = "rooms"

    id = db.Column(db.Integer, primary_key=True)
    residence = db.Column(db.Integer, db.ForeignKey("residences.id"), nullable=False)
    room_type = db.Column(
        db.Enum(RoomTypeEnum), db.ForeignKey("roomTypes.room_type"), nullable=False
    )
    rent = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(300), nullable=True)

    def to_dict(self):
        pass
