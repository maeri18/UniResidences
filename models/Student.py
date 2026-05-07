from models import db


class Student(db.Model):
    __tablename__ = "students"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    application_id = db.Column(
        db.Integer, db.ForeignKey("applications.id"), nullable=True
    )

    def to_dict(self):
        pass
