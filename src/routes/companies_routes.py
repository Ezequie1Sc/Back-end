from flask import request
from flask_restx import Namespace, Resource
from extensions import db
from models.company import Company

companies_ns = Namespace("companies", description="Gestión de empresas")

@companies_ns.route('/')
class CompanyList(Resource):
    def get(self):
        companies = Company.query.all()
        return [{
            "id": str(c.id),
            "name": c.name,
            "sector": c.sector,
            "contact_name": c.contact_name,
            "contact_phone": c.contact_phone,
            "logo_url": c.logo_url
        } for c in companies]

    def post(self):
        data = request.get_json()

        c = Company(
            name=data["name"],
            sector=data.get("sector"),
            contact_name=data.get("contact_name"),
            contact_phone=data.get("contact_phone")
        )
        db.session.add(c)
        db.session.commit()

        return {"id": str(c.id)}, 201


@companies_ns.route('/<string:company_id>')
class CompanyResource(Resource):
    def get(self, company_id):
        c = Company.query.get(company_id)
        if not c:
            return {"error": "Empresa no encontrada"}, 404

        return {
            "id": str(c.id),
            "name": c.name,
            "sector": c.sector,
            "contact_name": c.contact_name,
            "contact_phone": c.contact_phone,
            "logo_url": c.logo_url
        }

    def delete(self, company_id):
        c = Company.query.get(company_id)
        if not c:
            return {"error": "Empresa no encontrada"}, 404

        db.session.delete(c)
        db.session.commit()

        return {"msg": "Empresa eliminada"}
