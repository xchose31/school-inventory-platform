from flask_login import current_user
import os
import uuid
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf', 'ppt', 'pptx', 'doc', 'docx', 'txt'}


def check_roles():
    roles = []
    if not current_user.is_authenticated:
        return None
    empl = current_user.person.emp_status
    if empl.is_teacher:
        roles.append('teacher')
    if empl.is_technician:
        roles.append('technician')
    return roles


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def save_file(file, type):
    if allowed_file(file.filename):
        upload_folder = ''
        if type == 'equipment':
            upload_folder = os.path.join('app', 'static', 'uploads', 'equipment')
        elif type == 'material':
            upload_folder = os.path.join('app', 'static', 'uploads', 'materials')
        if not upload_folder:
            return None
        filename = secure_filename(file.filename)

        ext = filename.rsplit('.', 1)[1].lower()
        unique_filename = f"{uuid.uuid4().hex}.{ext}"

        os.makedirs(upload_folder, exist_ok=True)

        file_path = os.path.join(upload_folder, unique_filename)

        file.save(file_path)

        image_filename = unique_filename
        return image_filename
    return None
