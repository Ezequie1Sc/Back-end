import os
import uuid
from decimal import Decimal
from datetime import datetime, time

from flask import Flask, request, send_file, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api, Resource, fields
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.exceptions import NotFound
from flask_cors import CORS
from sqlalchemy import func

# -----------------------
# Config
# -----------------------
app = Flask(__name__)
CORS(app)

# Ajusta esta URI si tu DB es distinta
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:root@localhost:5432/companyTest"
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Uploads (logos)
UPLOAD_FOLDER = 'uploads/logos'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5MB

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# -----------------------
# DB init
# -----------------------
db = SQLAlchemy(app)
api = Api(app, version='1.0', title='API ASG', description='API para autodiagnóstico ASG')

# -----------------------
# Models (coinciden con tu esquema)
# -----------------------
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

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

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.Text, nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)
    company_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey('companies.id'))
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

class Area(db.Model):
    __tablename__ = 'areas'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(5), unique=True, nullable=False)  # A, S, G
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)

class Level(db.Model):
    __tablename__ = 'levels'
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(50), unique=True, nullable=False)  # basic...
    label = db.Column(db.String(50), nullable=False)
    score = db.Column(db.Numeric, nullable=False)

class Indicator(db.Model):
    __tablename__ = 'indicators'
    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    area_id = db.Column(db.Integer, db.ForeignKey('areas.id'), nullable=False)
    question = db.Column(db.Text, nullable=False)
    display_order = db.Column(db.Integer, default=0)
    active = db.Column(db.Boolean, default=True)
    created_by = db.Column(db.UUID(as_uuid=True), db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

class Evaluation(db.Model):
    __tablename__ = 'evaluations'
    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    company_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey('companies.id'), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    semester = db.Column(db.Integer, nullable=False)
    created_by = db.Column(db.UUID(as_uuid=True), db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=db.func.now())
    __table_args__ = (db.UniqueConstraint('company_id', 'year', 'semester', name='uix_company_year_semester'),)

class Answer(db.Model):
    __tablename__ = 'answers'
    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    evaluation_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey('evaluations.id'), nullable=False)
    indicator_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey('indicators.id'), nullable=False)
    level_id = db.Column(db.Integer, db.ForeignKey('levels.id'), nullable=False)
    numeric_value = db.Column(db.Numeric, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())
    __table_args__ = (db.UniqueConstraint('evaluation_id', 'indicator_id', name='uix_eval_indicator'),)

class EvaluationStats(db.Model):
    __tablename__ = 'evaluation_stats'
    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    evaluation_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey('evaluations.id'), unique=True, nullable=False)
    avg_environmental = db.Column(db.Numeric)
    avg_social = db.Column(db.Numeric)
    avg_governance = db.Column(db.Numeric)
    avg_global = db.Column(db.Numeric)
    classification_environmental = db.Column(db.String(50))
    classification_social = db.Column(db.String(50))
    classification_governance = db.Column(db.String(50))
    classification_global = db.Column(db.String(50))
    calculated_at = db.Column(db.DateTime, default=db.func.now())

# -----------------------
# Helpers
# -----------------------
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def classify(avg):
    if avg is None:
        return None
    a = float(avg)
    if 6 <= a <= 7.4:
        return "Básico"
    if 7.5 <= a <= 9.4:
        return "Intermedio"
    if a >= 9.5:
        return "Avanzado"
    return "Desconocido"

def is_admin_by_role(role_name):
    return role_name == 'admin'

# -----------------------
# Seed inicial (areas, levels, roles, admin)
# -----------------------
def seed_initial():
    # Areas
    if Area.query.count() == 0:
        db.session.add_all([
            Area(code='A', name='Ambiental', description='Ámbito Ambiental'),
            Area(code='S', name='Social', description='Ámbito Social'),
            Area(code='G', name='Gobernanza', description='Ámbito Gobernanza'),
        ])
    # Levels
    if Level.query.count() == 0:
        db.session.add_all([
            Level(key='basic', label='Básico', score=6),
            Level(key='intermediate', label='Intermedio', score=8),
            Level(key='advanced', label='Avanzado', score=10),
        ])
    # Roles
    if Role.query.count() == 0:
        db.session.add_all([Role(name='admin'), Role(name='company')])
    db.session.commit()

    # Default admin (si no existe)
    admin_email = os.getenv('ADMIN_EMAIL', 'admin@company.test')
    admin_pw = os.getenv('ADMIN_PW', 'admin1234')
    if not User.query.filter_by(email=admin_email).first():
        role_admin = Role.query.filter_by(name='admin').first()
        u = User(email=admin_email, password_hash=generate_password_hash(admin_pw), role_id=role_admin.id)
        db.session.add(u)
        db.session.commit()
        print(f"Admin creado: {admin_email} / {admin_pw}")

# -----------------------
# API Models (Flask-RESTX)
# -----------------------
usuario_model = api.model('User', {
    'id': fields.String(readonly=True),
    'email': fields.String(required=True),
    'role_id': fields.Integer,
    'company_id': fields.String
})

register_model = api.model('Register', {
    'company_name': fields.String(required=True),
    'email': fields.String(required=True),
    'password': fields.String(required=True)
})

login_model = api.model('Login', {
    'email': fields.String(required=True),
    'password': fields.String(required=True)
})

company_model = api.model('Company', {
    'id': fields.String(readonly=True),
    'name': fields.String(required=True),
    'sector': fields.String,
    'contact_name': fields.String,
    'contact_phone': fields.String,
    'logo_url': fields.String
})

indicator_model = api.model('Indicator', {
    'id': fields.String(readonly=True),
    'area_id': fields.Integer(required=True),
    'question': fields.String(required=True),
    'display_order': fields.Integer
})

level_model = api.model('Level', {
    'id': fields.Integer(readonly=True),
    'key': fields.String,
    'label': fields.String,
    'score': fields.Float
})

evaluation_input_model = api.model('EvaluationInput', {
    'year': fields.Integer(required=True),
    'semester': fields.Integer(required=True),
    'created_by': fields.String(required=True),
    'answers': fields.List(fields.Nested(api.model('AnswerIn', {
        'indicator_id': fields.String(required=True),
        'level_id': fields.Integer(required=True)
    })))
})

# -----------------------
# Namespaces
# -----------------------
auth_ns = api.namespace('auth', description='Autenticación')
companies_ns = api.namespace('companies', description='Empresas')
indicators_ns = api.namespace('indicators', description='Indicadores')
levels_ns = api.namespace('levels', description='Niveles')
evaluations_ns = api.namespace('evaluations', description='Evaluaciones')
upload_ns = api.namespace('upload', description='Upload')

# -----------------------
# Auth endpoints (register/login) - no JWT; mimetiza SIGEL
# -----------------------
@auth_ns.route('/register')
class Register(Resource):
    @auth_ns.expect(register_model, validate=True)
    def post(self):
        data = request.get_json()
        company_name = data.get('company_name')
        email = data.get('email')
        password = data.get('password')

        if not company_name or not email or not password:
            return {'error': 'Campos requeridos faltantes'}, 400

        if User.query.filter_by(email=email).first():
            return {'error': 'Email ya registrado'}, 400

        # Crear empresa
        company = Company(name=company_name)
        db.session.add(company)
        db.session.flush()  # obtener company.id

        # asignar role company
        role_company = Role.query.filter_by(name='company').first()
        user = User(email=email, password_hash=generate_password_hash(password), role_id=role_company.id, company_id=company.id)
        db.session.add(user)
        db.session.commit()
        return {'msg': 'Registrado', 'company_id': str(company.id)}, 201

@auth_ns.route('/login')
class Login(Resource):
    @auth_ns.expect(login_model, validate=True)
    def post(self):
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        if not email or not password:
            return {'error': 'Campos requeridos faltantes'}, 400
        user = User.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password_hash, password):
            return {'error': 'Usuario o contraseña incorrectos'}, 401
        # devolvemos info básica del usuario (sin tokens)
        return {
            'id': str(user.id),
            'email': user.email,
            'role_id': user.role_id,
            'company_id': str(user.company_id) if user.company_id else None
        }, 200

# -----------------------
# Companies endpoints
# -----------------------
@companies_ns.route('/')
class CompanyList(Resource):
    def get(self):
        companies = Company.query.all()
        out = []
        for c in companies:
            out.append({
                'id': str(c.id),
                'name': c.name,
                'sector': c.sector,
                'contact_name': c.contact_name,
                'contact_phone': c.contact_phone,
                'logo_url': c.logo_url
            })
        return out

    @companies_ns.expect(company_model, validate=True)
    def post(self):
        data = request.get_json()
        if not data or not data.get('name'):
            return {'error': 'Nombre requerido'}, 400
        c = Company(
            name=data['name'],
            sector=data.get('sector'),
            contact_name=data.get('contact_name'),
            contact_phone=data.get('contact_phone')
        )
        db.session.add(c)
        db.session.commit()
        return {'id': str(c.id)}, 201

@companies_ns.route('/<string:company_id>')
class CompanyResource(Resource):
    def get(self, company_id):
        c = Company.query.get(company_id)
        if not c:
            raise NotFound("Empresa no encontrada")
        return {
            'id': str(c.id),
            'name': c.name,
            'sector': c.sector,
            'contact_name': c.contact_name,
            'contact_phone': c.contact_phone,
            'logo_url': c.logo_url
        }

    def delete(self, company_id):
        c = Company.query.get(company_id)
        if not c:
            raise NotFound("Empresa no encontrada")
        db.session.delete(c)
        db.session.commit()
        return {'msg': 'Empresa eliminada'}

# -----------------------
# Users endpoints (admin may manage)
# -----------------------
@auth_ns.route('/users')
class UserList(Resource):
    def get(self):
        users = User.query.all()
        out = []
        for u in users:
            out.append({
                'id': str(u.id),
                'email': u.email,
                'role_id': u.role_id,
                'company_id': str(u.company_id) if u.company_id else None
            })
        return out

    @auth_ns.expect(usuario_model := api.model('UserCreate', {
        'email': fields.String(required=True),
        'password': fields.String(required=True),
        'role_id': fields.Integer(required=True),
        'company_id': fields.String
    }), validate=True)
    def post(self):
        data = request.get_json()
        if User.query.filter_by(email=data['email']).first():
            return {'error': 'Email ya registrado'}, 400
        user = User(
            email=data['email'],
            password_hash=generate_password_hash(data['password']),
            role_id=data['role_id'],
            company_id=data.get('company_id')
        )
        db.session.add(user)
        db.session.commit()
        return {'id': str(user.id)}, 201

@auth_ns.route('/users/<string:user_id>')
class UserResource(Resource):
    def get(self, user_id):
        u = User.query.get(user_id)
        if not u:
            raise NotFound("Usuario no encontrado")
        return {'id': str(u.id), 'email': u.email, 'role_id': u.role_id, 'company_id': str(u.company_id) if u.company_id else None}

    def delete(self, user_id):
        u = User.query.get(user_id)
        if not u:
            raise NotFound("Usuario no encontrado")
        db.session.delete(u)
        db.session.commit()
        return {'msg': 'Usuario eliminado'}

# -----------------------
# Indicators endpoints
# -----------------------
@indicators_ns.route('/')
class IndicatorList(Resource):
    def get(self):
        inds = Indicator.query.filter_by(active=True).order_by(Indicator.display_order).all()
        out = []
        for i in inds:
            out.append({
                'id': str(i.id),
                'area_id': i.area_id,
                'question': i.question,
                'display_order': i.display_order
            })
        return out

    @indicators_ns.expect(indicator_model, validate=True)
    def post(self):
        data = request.get_json()
        # created_by optional - pass user id in payload
        ind = Indicator(area_id=data['area_id'], question=data['question'], display_order=data.get('display_order', 0), created_by=data.get('created_by'))
        db.session.add(ind)
        db.session.commit()
        return {'id': str(ind.id)}, 201

@indicators_ns.route('/<string:indicator_id>')
class IndicatorResource(Resource):
    def get(self, indicator_id):
        i = Indicator.query.get(indicator_id)
        if not i:
            raise NotFound("Indicador no encontrado")
        return {'id': str(i.id), 'area_id': i.area_id, 'question': i.question, 'active': i.active}

    def delete(self, indicator_id):
        i = Indicator.query.get(indicator_id)
        if not i:
            raise NotFound("Indicador no encontrado")
        i.active = False
        db.session.commit()
        return {'msg': 'Indicador desactivado'}

# -----------------------
# Levels endpoints
# -----------------------
@levels_ns.route('/')
class LevelList(Resource):
    def get(self):
        lvls = Level.query.all()
        out = []
        for l in lvls:
            out.append({'id': l.id, 'key': l.key, 'label': l.label, 'score': float(l.score)})
        return out

# -----------------------
# Evaluations endpoints
# -----------------------
@evaluations_ns.route('/')
class EvaluationCreate(Resource):
    @evaluations_ns.expect(evaluation_input_model, validate=True)
    def post(self):
        data = request.get_json()
        year = data.get('year')
        semester = data.get('semester')
        created_by = data.get('created_by')
        answers = data.get('answers', [])

        # created_by must exist (user)
        if not created_by:
            return {'error': 'created_by (user id) es requerido'}, 400

        user = User.query.get(created_by)
        if not user or not user.company_id:
            return {'error': 'Usuario inválido o sin empresa asociada'}, 400

        # unique check
        exists = Evaluation.query.filter_by(company_id=user.company_id, year=year, semester=semester).first()
        if exists:
            return {'error': 'Evaluación ya existe para esa empresa y semestre'}, 400

        eval_ = Evaluation(company_id=user.company_id, year=year, semester=semester, created_by=created_by)
        db.session.add(eval_)
        db.session.flush()

        # insert answers
        for a in answers:
            ind = Indicator.query.get(a['indicator_id'])
            lvl = Level.query.get(a['level_id'])
            if not ind or not lvl:
                db.session.rollback()
                return {'error': 'Indicador o nivel inválido'}, 400
            ans = Answer(evaluation_id=eval_.id, indicator_id=ind.id, level_id=lvl.id, numeric_value=lvl.score)
            db.session.add(ans)

        db.session.flush()

        # calculate averages grouped by area code (A,S,G)
        q = db.session.query(Area.code.label('code'), func.avg(Answer.numeric_value).label('avg')) \
            .join(Indicator, Indicator.area_id == Area.id) \
            .join(Answer, Answer.indicator_id == Indicator.id) \
            .filter(Answer.evaluation_id == eval_.id) \
            .group_by(Area.code).all()

        avgs = {row.code: float(row.avg) for row in q}
        avg_env = avgs.get('A')
        avg_soc = avgs.get('S')
        avg_gov = avgs.get('G')
        avg_global = None
        if len(avgs) > 0:
            avg_global = sum(avgs.values()) / len(avgs)

        stats = EvaluationStats(
            evaluation_id=eval_.id,
            avg_environmental=avg_env,
            avg_social=avg_soc,
            avg_governance=avg_gov,
            avg_global=avg_global,
            classification_environmental=classify(avg_env),
            classification_social=classify(avg_soc),
            classification_governance=classify(avg_gov),
            classification_global=classify(avg_global)
        )
        db.session.add(stats)
        db.session.commit()

        return {
            'evaluation_id': str(eval_.id),
            'stats': {
                'avg_environmental': avg_env,
                'avg_social': avg_soc,
                'avg_governance': avg_gov,
                'avg_global': avg_global,
                'classification_environmental': stats.classification_environmental,
                'classification_social': stats.classification_social,
                'classification_governance': stats.classification_governance,
                'classification_global': stats.classification_global
            }
        }, 201

@evaluations_ns.route('/company/<string:company_id>')
class EvaluationsByCompany(Resource):
    def get(self, company_id):
        evals = Evaluation.query.filter_by(company_id=company_id).order_by(Evaluation.year.desc(), Evaluation.semester.desc()).all()
        out = []
        for e in evals:
            s = EvaluationStats.query.filter_by(evaluation_id=e.id).first()
            out.append({
                'id': str(e.id),
                'year': e.year,
                'semester': e.semester,
                'created_at': e.created_at.isoformat(),
                'stats': {
                    'avg_environmental': float(s.avg_environmental) if s and s.avg_environmental is not None else None,
                    'avg_social': float(s.avg_social) if s and s.avg_social is not None else None,
                    'avg_governance': float(s.avg_governance) if s and s.avg_governance is not None else None,
                    'avg_global': float(s.avg_global) if s and s.avg_global is not None else None,
                    'classification_global': s.classification_global if s else None
                }
            })
        return out


@upload_ns.route('/logo')
class UploadLogo(Resource):
    def post(self):
        # se espera 'company_id' en form o query + file en 'file'
        company_id = request.form.get('company_id') or request.args.get('company_id')
        if not company_id:
            return {'error': 'company_id requerido (form-data o query)'}, 400
        c = Company.query.get(company_id)
        if not c:
            return {'error': 'Empresa no encontrada'}, 404

        if 'file' not in request.files:
            return {'error': 'No se recibió archivo'}, 400
        file = request.files['file']
        if file.filename == '':
            return {'error': 'Archivo sin nombre'}, 400
        ext = file.filename.rsplit('.', 1)[1].lower() if '.' in file.filename else ''
        if ext not in ALLOWED_EXTENSIONS:
            return {'error': f'Extensión no permitida: {ext}'}, 400

        filename = secure_filename(file.filename)
        uniq = f"{int(datetime.now().timestamp())}_{uuid.uuid4().hex}.{ext}"
        save_path = os.path.join(app.config['UPLOAD_FOLDER'], uniq)
        try:
            file.save(save_path)
        except Exception as e:
            return {'error': f'Error guardando archivo: {str(e)}'}, 500

        # Guardar solo el nombre (frontend puede solicitar /upload/logo/<filename>)
        c.logo_url = uniq
        db.session.commit()
        return {'logo_url': c.logo_url}, 200

@upload_ns.route('/logo/<string:filename>')
class GetLogo(Resource):
    def get(self, filename):
        path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if not os.path.exists(path):
            return {'error': 'Archivo no encontrado'}, 404
        return send_file(path, as_attachment=True, download_name=filename)

# -----------------------
# Registrar namespaces
# -----------------------
api.add_namespace(auth_ns, path='/auth')
api.add_namespace(companies_ns, path='/companies')
api.add_namespace(indicators_ns, path='/indicators')
api.add_namespace(levels_ns, path='/levels')
api.add_namespace(evaluations_ns, path='/evaluations')
api.add_namespace(upload_ns, path='/upload')

# 
@app.route('/healthcheck')
def healthcheck():
    try:
        db.session.execute('SELECT 1')
        return {'status': 'OK', 'database': 'connected'}
    except Exception as e:
        return {'status': 'Error', 'message': str(e)}, 500




if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        seed_initial()  
    app.run(debug=True, host='0.0.0.0', port=5000)