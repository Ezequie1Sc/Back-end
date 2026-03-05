from datetime import datetime
import uuid
import os
from werkzeug.utils import secure_filename

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

def allowed_file(filename, allowed_ext):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_ext
