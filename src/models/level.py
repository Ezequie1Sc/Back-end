from extensions import db

class Level(db.Model):
    __tablename__ = 'levels'
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(50), unique=True, nullable=False)
    label = db.Column(db.String(50), nullable=False)
    score = db.Column(db.Numeric, nullable=False)
