import uuid
from extensions import db

class Indicator(db.Model):
    __tablename__ = 'indicators'
    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    area_id = db.Column(db.Integer, db.ForeignKey('areas.id'), nullable=False)
    question = db.Column(db.Text, nullable=False)
    display_order = db.Column(db.Integer, default=0)
    active = db.Column(db.Boolean, default=True)
    created_by = db.Column(db.UUID(as_uuid=True), db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
