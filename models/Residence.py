from models import db


class Residence(db.Model):
    __tablename__ = "residences"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)

    def to_dict(self):
        pass
