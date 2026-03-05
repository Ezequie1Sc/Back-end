import os
from werkzeug.security import generate_password_hash
from extensions import db
from models import Area, Level, Role, User

def seed_initial():
    if Area.query.count() == 0:
        db.session.add_all([
            Area(code='A', name='Ambiental', description='Ámbito Ambiental'),
            Area(code='S', name='Social', description='Ámbito Social'),
            Area(code='G', name='Gobernanza', description='Ámbito Gobernanza'),
        ])

    if Level.query.count() == 0:
        db.session.add_all([
            Level(key='basic', label='Básico', score=6),
            Level(key='intermediate', label='Intermedio', score=8),
            Level(key='advanced', label='Avanzado', score=10),
        ])

    if Role.query.count() == 0:
        db.session.add_all([Role(name='admin'), Role(name='company')])

    db.session.commit()

    admin_email = os.getenv('ADMIN_EMAIL', 'admin@company.test')
    admin_pw = os.getenv('ADMIN_PW', 'admin1234')

    if not User.query.filter_by(email=admin_email).first():
        role_admin = Role.query.filter_by(name='admin').first()
        db.session.add(
            User(
                email=admin_email,
                password_hash=generate_password_hash(admin_pw),
                role_id=role_admin.id
            )
        )
        db.session.commit()
