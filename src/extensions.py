from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api

db = SQLAlchemy()
api = Api(
    version='1.0',
    title='API ASG',
    description='API para autodiagnóstico ASG'
)
