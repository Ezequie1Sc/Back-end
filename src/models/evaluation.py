import uuid
from extensions import db

class Evaluation(db.Model):
    __tablename__ = 'evaluations'
    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    company_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey('companies.id'), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    semester = db.Column(db.Integer, nullable=False)
    created_by = db.Column(db.UUID(as_uuid=True), db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=db.func.now())
    __table_args__ = (
        db.UniqueConstraint('company_id', 'year', 'semester', name='uix_company_year_semester'),
    )
