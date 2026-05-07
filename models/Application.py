from models import db
import enum


class Status(enum.Enum):
    ACCEPTED = "Accepted"
    REJECTED = "Rejected"
    PENDING = "Pending"


class Application(db.Model):
    __tablename__ = "applications"

    id = db.Column(db.Integer, primary_key=True)
    room = db.Column(db.Integer, db.ForeignKey("rooms.id"), nullable=False)
    contract_id = db.Column(db.Integer, db.ForeignKey("contracts.id"), nullable=True)
    status = db.Column(db.Enum(Status), nullable=False)
    submission_date = db.Column(db.DateTime)
    expiration_date = db.Column(db.DateTime)

    def to_dict(self):
        pass
