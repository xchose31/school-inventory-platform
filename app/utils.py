from flask_login import current_user


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
