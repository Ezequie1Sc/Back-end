import uuid
from extensions import db

class Answer(db.Model):
    __tablename__ = 'answers'
    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    evaluation_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey('evaluations.id'), nullable=False)
    indicator_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey('indicators.id'), nullable=False)
    level_id = db.Column(db.Integer, db.ForeignKey('levels.id'), nullable=False)
    numeric_value = db.Column(db.Numeric, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())
    __table_args__ = (
        db.UniqueConstraint('evaluation_id', 'indicator_id', name='uix_eval_indicator'),
    )
