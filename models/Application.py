from models import db
import enum
from sqlalchemy.orm import Mapped


class ApplicationStatus(enum.Enum):
    ACCEPTED = "Accepted"
    REJECTED = "Rejected"
    PENDING = "Pending"


class Application(db.Model):
    __tablename__ = "applications"

    application_Id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Enum(ApplicationStatus), nullable=False)
    reason_for_refusal = db.Column(db.String(300), nullable=True)
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
        if self.status == ApplicationStatus.PENDING:
            return {
                "application_Id": self.application_Id,
                "status": self.status,
                "submission_date": self.submission_date,
                "student_name": self.wasSubmittedBy.student_name,
                "room_id": self.room_Id,
            }
        if self.status == ApplicationStatus.ACCEPTED:
            return {
                "application_Id": self.application_Id,
                "status": self.status,
                "submission_date": self.submission_date,
                "student_name": self.wasSubmittedBy.student_name,
                "room_id": self.room_Id,
                "handled_by": self.admin_Id,
            }
        if self.status == ApplicationStatus.REJECTED:
            return {
                "application_Id": self.application_Id,
                "status": self.status,
                "submission_date": self.submission_date,
                "student_name": self.wasSubmittedBy.student_name,
                "room_id": self.room_Id,
                "handled_by": self.admin_Id,
                "reason_for_refusal": self.reason_for_refusal,
            }
