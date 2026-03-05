from flask import request
from flask_restx import Namespace, Resource, fields
from werkzeug.security import generate_password_hash, check_password_hash

from extensions import db
from models.user import User
from models.company import Company
from models.role import Role

auth_ns = Namespace("auth", description="Autenticación")

login_model = auth_ns.model("Login", {
    "email": fields.String(required=True),
    "password": fields.String(required=True)
})

register_model = auth_ns.model("Register", {
    "company_name": fields.String(required=True),
    "email": fields.String(required=True),
    "password": fields.String(required=True)
})

@auth_ns.route("/register")
class Register(Resource):
    @auth_ns.expect(register_model, validate=True)
    def post(self):
        data = request.json

        if User.query.filter_by(email=data["email"]).first():
            return {"error": "Email ya registrado"}, 400

        company = Company(name=data["company_name"])
        db.session.add(company)
        db.session.flush()

        role = Role.query.filter_by(name="company").first()
        user = User(
            email=data["email"],
            password_hash=generate_password_hash(data["password"]),
            role_id=role.id,
            company_id=company.id
        )

        db.session.add(user)
        db.session.commit()
        return {"company_id": str(company.id)}, 201
