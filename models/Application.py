from models import db
import enum
from sqlalchemy.orm import Mapped
from helper_functions import date_to_formatted_str
import random



class ApplicationStatus(enum.Enum):
    ACCEPTED = "Accepted"
    REJECTED = "Rejected"
    PENDING = "Pending"

def generate_random_application_id():
    return random.randint(100,10000)

class Application(db.Model):
    __tablename__ = "applications"

    application_Id = db.Column(db.Integer, primary_key=True,autoincrement=False, default=generate_random_application_id)
    status = db.Column(db.Enum(ApplicationStatus), nullable=False)
    reason_for_refusal = db.Column(db.String(300), nullable=True)
    application_message = db.Column(db.String(500), nullable=False)
    submission_date = db.Column(db.DateTime, nullable=False)

    student_Id: Mapped[int] = db.Column(
        db.Integer, db.ForeignKey("students.student_Id"), nullable=False
    )
    wasSubmittedBy: Mapped["Student"] = db.relationship(back_populates="submitted")

    room_Id: Mapped[int] = db.Column(
        db.Integer, db.ForeignKey("rooms.room_Id"), nullable=False
    )
    linksTo: Mapped["Room"] = db.relationship(back_populates="isLinkedTo")

    admin_Id: Mapped[int] = db.Column(
        db.Integer, db.ForeignKey("admins.admin_Id"), nullable=True
    )
    handledBy: Mapped["Admin"] = db.relationship(back_populates="handled")

    def to_dict(self):
        result_dict = {
            "application_Id": self.application_Id,
            "status": self.status.value,
            "submission_date": date_to_formatted_str(self.submission_date),
            "student_name": self.wasSubmittedBy.student_name,
            "room_id": self.room_Id,
            "application_message": self.application_message,
        }

        if self.status == ApplicationStatus.ACCEPTED:
            result_dict["handled_by"] = self.admin_Id

        elif self.status == ApplicationStatus.REJECTED:
            result_dict["handled_by"] = self.admin_Id
            result_dict["reason_for_refusal"] = self.reason_for_refusal

        return result_dict
