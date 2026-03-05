import os
import uuid
from flask import request, send_file
from flask_restx import Namespace, Resource
from extensions import db
from models.company import Company

upload_ns = Namespace("upload", description="Subida de archivos")

@upload_ns.route('/logo')
class UploadLogo(Resource):
    def post(self):
        company_id = request.form.get('company_id')
        c = Company.query.get(company_id)
        if not c:
            return {"error": "Empresa no encontrada"}, 404

        file = request.files["file"]
        ext = file.filename.split('.')[-1]
        filename = f"{uuid.uuid4()}.{ext}"

        upload_folder = "uploads/logos"
        os.makedirs(upload_folder, exist_ok=True)

        path = os.path.join(upload_folder, filename)
        file.save(path)

        c.logo_url = filename
        db.session.commit()

        return {"logo_url": filename}


@upload_ns.route('/logo/<string:filename>')
class Logo(Resource):
    def get(self, filename):
        path = os.path.join("uploads/logos", filename)
        if not os.path.exists(path):
            return {"error": "Archivo no encontrado"}, 404
        return send_file(path)
