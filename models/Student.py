from models import db
from sqlalchemy.orm import Mapped
from typing import List
import random

def generate_random_student_id():
    return random.randint(100,10000)

class Student(db.Model):
    __tablename__ = "students"

    student_Id = db.Column(db.Integer, primary_key=True, autoincrement=False,default=generate_random_student_id)
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
