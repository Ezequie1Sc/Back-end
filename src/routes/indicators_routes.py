from flask import request
from flask_restx import Namespace, Resource
from extensions import db
from models.indicator import Indicator

indicators_ns = Namespace("indicators", description="Indicadores ASG")

@indicators_ns.route('/')
class IndicatorList(Resource):
    def get(self):
        inds = Indicator.query.filter_by(active=True).order_by(Indicator.display_order).all()

        return [{
            "id": str(i.id),
            "area_id": i.area_id,
            "question": i.question,
            "display_order": i.display_order
        } for i in inds]

    def post(self):
        data = request.get_json()

        ind = Indicator(
            area_id=data["area_id"],
            question=data["question"],
            display_order=data.get("display_order", 0),
            created_by=data.get("created_by")
        )
        db.session.add(ind)
        db.session.commit()

        return {"id": str(ind.id)}, 201


@indicators_ns.route('/<string:indicator_id>')
class IndicatorResource(Resource):
    def get(self, indicator_id):
        i = Indicator.query.get(indicator_id)
        if not i:
            return {"error": "Indicador no encontrado"}, 404

        return {
            "id": str(i.id),
            "area_id": i.area_id,
            "question": i.question,
            "active": i.active
        }

    def delete(self, indicator_id):
        i = Indicator.query.get(indicator_id)
        if not i:
            return {"error": "Indicador no encontrado"}, 404

        i.active = False
        db.session.commit()

        return {"msg": "Indicador desactivado"}
