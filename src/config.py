import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:root@localhost:5432/companyTest"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    UPLOAD_FOLDER = 'uploads/logos'
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024
