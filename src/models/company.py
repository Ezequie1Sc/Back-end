import uuid
from extensions import db

class Company(db.Model):
    __tablename__ = 'companies'
    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(255), nullable=False)
    sector = db.Column(db.String(255))
    contact_name = db.Column(db.String(255))
    contact_phone = db.Column(db.String(50))
    logo_url = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
