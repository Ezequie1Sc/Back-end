from flask import request
from flask_restx import Namespace, Resource
from sqlalchemy import func
from extensions import db
from models.evaluation import Evaluation
from models.answer import Answer
from models.indicator import Indicator
from models.level import Level
from models.area import Area
from models.user import User
from models.evaluation_stats import EvaluationStats

evaluations_ns = Namespace("evaluations", description="Evaluaciones ASG")

@evaluations_ns.route('/')
class EvaluationCreate(Resource):
    def post(self):
        data = request.get_json()

        user = User.query.get(data["created_by"])
        if not user or not user.company_id:
            return {"error": "Usuario inválido"}, 400

        eval_ = Evaluation(
            company_id=user.company_id,
            year=data["year"],
            semester=data["semester"],
            created_by=data["created_by"]
        )
        db.session.add(eval_)
        db.session.flush()

        for a in data["answers"]:
            lvl = Level.query.get(a["level_id"])
            ans = Answer(
                evaluation_id=eval_.id,
                indicator_id=a["indicator_id"],
                level_id=lvl.id,
                numeric_value=lvl.score
            )
            db.session.add(ans)

        q = db.session.query(
            Area.code,
            func.avg(Answer.numeric_value)
        ).join(Indicator, Indicator.area_id == Area.id)\
         .join(Answer, Answer.indicator_id == Indicator.id)\
         .filter(Answer.evaluation_id == eval_.id)\
         .group_by(Area.code).all()

        avgs = {code: float(avg) for code, avg in q}
        avg_global = sum(avgs.values()) / len(avgs) if avgs else None

        stats = EvaluationStats(
            evaluation_id=eval_.id,
            avg_environmental=avgs.get("A"),
            avg_social=avgs.get("S"),
            avg_governance=avgs.get("G"),
            avg_global=avg_global
        )
        db.session.add(stats)
        db.session.commit()

        return {"evaluation_id": str(eval_.id)}, 201


@evaluations_ns.route('/company/<string:company_id>')
class EvaluationsByCompany(Resource):
    def get(self, company_id):

        evals = Evaluation.query.filter_by(company_id=company_id)\
            .order_by(Evaluation.year.desc(), Evaluation.semester.desc()).all()

        out = []
        for e in evals:
            s = EvaluationStats.query.filter_by(evaluation_id=e.id).first()
            out.append({
                "id": str(e.id),
                "year": e.year,
                "semester": e.semester,
                "created_at": e.created_at.isoformat(),
                "stats": {
                    "avg_environmental": float(s.avg_environmental) if s else None,
                    "avg_social": float(s.avg_social) if s else None,
                    "avg_governance": float(s.avg_governance) if s else None,
                    "avg_global": float(s.avg_global) if s else None
                }
            })

        return out
