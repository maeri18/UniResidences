from models import db
from sqlalchemy.orm import Mapped
from typing import List


class Student(db.Model):
    __tablename__ = "students"

    student_Id = db.Column(db.Integer, primary_key=True)
    student_name = db.Column(db.String(100), nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    submitted: Mapped[List["Application"]] = db.relationship(
        back_populates="wasSubmittedBy"
    )

    def to_dict(self):
        return {
            "id": self.student_Id,
            "name": self.student_name,
            "applications": [
                application.application_Id for application in self.submitted
            ],
        }
