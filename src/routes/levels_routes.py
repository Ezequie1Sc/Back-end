from flask_restx import Namespace, Resource
from models.level import Level

levels_ns = Namespace("levels", description="Niveles de madurez")

@levels_ns.route('/')
class LevelList(Resource):
    def get(self):
        lvls = Level.query.all()

        return [{
            "id": l.id,
            "key": l.key,
            "label": l.label,
            "score": float(l.score)
        } for l in lvls]
