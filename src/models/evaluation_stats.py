import uuid
from extensions import db

class EvaluationStats(db.Model):
    __tablename__ = 'evaluation_stats'
    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    evaluation_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey('evaluations.id'), unique=True, nullable=False)
    avg_environmental = db.Column(db.Numeric)
    avg_social = db.Column(db.Numeric)
    avg_governance = db.Column(db.Numeric)
    avg_global = db.Column(db.Numeric)
    classification_environmental = db.Column(db.String(50))
    classification_social = db.Column(db.String(50))
    classification_governance = db.Column(db.String(50))
    classification_global = db.Column(db.String(50))
    calculated_at = db.Column(db.DateTime, default=db.func.now())
