import os
from flask import Flask
from flask_cors import CORS

from config import Config
from extensions import db, api
from seed import seed_initial

import models

from routes.auth_routes import auth_ns
from routes.companies_routes import companies_ns
from routes.indicators_routes import indicators_ns
from routes.levels_routes import levels_ns
from routes.evaluations_routes import evaluations_ns
from routes.upload_routes import upload_ns

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app)

    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    db.init_app(app)
    api.init_app(app)

    api.add_namespace(auth_ns, path='/auth')
    api.add_namespace(companies_ns, path='/companies')
    api.add_namespace(indicators_ns, path='/indicators')
    api.add_namespace(levels_ns, path='/levels')
    api.add_namespace(evaluations_ns, path='/evaluations')
    api.add_namespace(upload_ns, path='/upload')

    @app.route('/healthcheck')
    def healthcheck():
        db.session.execute('SELECT 1')
        return {'status': 'OK'}

    return app

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        seed_initial()
    app.run(debug=True, host='0.0.0.0', port=5000)
