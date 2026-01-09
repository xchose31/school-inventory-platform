import os.path
from functools import wraps
from .utils import save_file
from app import app, db
from flask import render_template, flash, redirect, url_for, abort, request, send_file
from flask_login import login_user, logout_user, current_user, login_required
from app.forms import LoginForm, EquipmentForm
import sqlalchemy as sa
from app.models import User, Equipment, ComPerson, RepairRequest
from app.qr import generate_qr_code
import requests


def user_is_employer():
    def decorator(f):
        @wraps(f)
        def decorated_func(*args, **kwargs):
            if not (current_user.is_authenticated and current_user.person.emp_status.active):
                abort(403)
            return f(*args, **kwargs)

        return decorated_func

    return decorator


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == form.username.data)
        )
        if user is not None:
            if user.username not in ['admin', 'student', 'technician']:
                data = {'ver': '1.0',
                        'get': 'auth',
                        'username': str(user.username),
                        'password': str(form.password.data)}
                req = requests.get('https://lis.1502.moscow/api/auth.php', params=data)
                if req.status_code == 200:
                    data = {'ver': '1.0',
                            'auth_code': req.json()['auth_code']}
                    req2 = requests.get('https://lis.1502.moscow/api/auth.php', params=data)
                    if req2.status_code == 200:
                        user_id = req2.json()['uid']
                        login_user(user, remember=form.remember_me.data)
                        return redirect(url_for('index'))
                    else:
                        flash('Invalid username or password')
                        return redirect(url_for('login'))
                else:
                    flash('Invalid username or password')
                    return redirect(url_for('login'))
            else:
                login_user(user, remember=form.remember_me.data)
                return redirect(url_for('index'))
        flash('Invalid username or password')
        return redirect(url_for('login'))
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/add_equipment', methods=['GET', 'POST'])
@user_is_employer()
def add_equipment():
    form = EquipmentForm()
    if form.validate_on_submit():
        equipment = Equipment(
            name=form.name.data,
            territory=form.territory.data,
            office=form.office.data,
            description=form.description.data
        )
        image = form.image.data
        save = save_file(image, 'equipment')
        if save:
            equipment.photo_path = save

        db.session.add(equipment)
        db.session.commit()
        return redirect(f'equipment/{equipment.id}')
    return render_template('add_equipment.html', form=form)


@app.route('/equipment/<int:id>')
def equipment(id):
    equipment = Equipment.query.get_or_404(id)
    repair_requests = db.session.query(RepairRequest) \
        .filter(RepairRequest.equipment_id == equipment.id) \
        .order_by(RepairRequest.is_completed.asc(), RepairRequest.creation_date.desc()) \
        .all()
    return render_template('equipment.html', equipment=equipment, repair_requests=repair_requests)


@app.route('/equipment/<int:id>/delete', methods=['GET', 'POST'])
@user_is_employer()
def delete_equipment(id):
    equipment = Equipment.query.get(id)
    equipment.is_deleted = True
    db.session.commit()
    flash('Оборудование успешно удалено!', 'success')
    return redirect(url_for('index'))


@app.route('/equipment/<int:id>/edit', methods=['GET', 'POST'])
@user_is_employer()
def edit_equipment(id):
    equipment = Equipment.query.get_or_404(id)
    form = EquipmentForm()

    if form.validate_on_submit():
        equipment.name = form.name.data
        equipment.territory = form.territory.data
        equipment.office = form.office.data
        equipment.description = form.description.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for(f'equipment', id=equipment.id))
    else:
        form.name.data = equipment.name
        form.territory.data = equipment.territory
        form.office.data = equipment.office
        form.description.data = equipment.description
        form.submit.label.text = 'Изменить'

    return render_template('add_equipment.html', form=form)


@app.route('/equipment_list')
@user_is_employer()
def equipment_list():
    equipments = Equipment.query.filter(Equipment.is_deleted == False).all()
    return render_template('equipment_list2.html', equipments=equipments)


@app.route('/equipment/<int:id>/qr')
@login_required
def equipment_qr(id):
    path = f'../qrcodes/qr_{id}.png'

    if not os.path.exists(path):
        generate_qr_code(id)

    return send_file(path, mimetype='image/png')


@app.route('/equipment/<int:id>/add_material')
@user_is_employer()
def add_material(id):
    pass


@app.route('/equipment/<int:id>/request_repair', methods=['GET', 'POST'])
@user_is_employer()
def create_repair_request(id):
    comment = request.form.get('comment', '').strip()
    priority = request.form.get('priority', 'средний')
    current_repair_requests = db.session.query(RepairRequest).filter(RepairRequest.is_completed == False).all()
    if current_repair_requests:
        flash('У этого оборудования уже есть невыполненная заявка на ремонт!', 'error')
        return redirect(url_for('equipment', id=id))
    repair_request = RepairRequest(
        equipment_id=id,
        comment=comment,
        priority=priority,
        user_id=current_user.id
    )
    db.session.add(repair_request)
    db.session.commit()

    flash('Заявка на ремонт успешно создана!', 'success')
    return redirect(url_for('equipment', id=id))


@app.route('/repair_requests')
@user_is_employer()
def repair_requests_list():
    if not current_user.person.emp_status.is_technician:
        abort(403)
    priority_order = sa.case(
        (RepairRequest.priority == 'критический', 1),
        (RepairRequest.priority == 'высокий', 2),
        (RepairRequest.priority == 'средний', 3),
        (RepairRequest.priority == 'низкий', 4),
        else_=5
    )
    repair_requests = db.session.query(RepairRequest).join(RepairRequest.equipment).order_by(
        RepairRequest.is_completed.asc(),
        priority_order.asc(),
        RepairRequest.creation_date.desc()
    ).all()

    return render_template('repair_requests.html', repair_requests=repair_requests)


@app.route('/repair_requests/<int:id>', methods=['GET', 'POST'])
@user_is_employer()
def repair_request_detail(id):
    req = RepairRequest.query.get_or_404(id)

    if request.method == 'POST':
        if not (current_user.is_authenticated and current_user.person.emp_status.is_technician):
            flash("У вас нет прав для завершения заявок.", "danger")
            return redirect(url_for('repair_request_detail', id=id))

        if not req.is_completed:
            completion_comment = request.form.get('completion_comment', '').strip()
            req.is_completed = True
            req.completion_date = db.func.now()
            req.completion_comment = completion_comment
            db.session.commit()
            flash("Заявка успешно отмечена как выполненная.", "success")
        return redirect(url_for('repair_request_detail', id=id))

    return render_template('repair_request_detail.html', repair_request=req)


@app.route('/complete_repair_request/<int:id>', methods=['GET', 'POST'])
@user_is_employer()
def complete_repair_request(id):
    req = RepairRequest.query.get_or_404(id)

    if request.method == 'POST':
        if not (current_user.is_authenticated and current_user.person.emp_status.is_technician):
            flash("У вас нет прав для завершения заявок.", "danger")
            return redirect(url_for('repair_request_detail', id=id))

        if not req.is_completed:
            completion_comment = request.form.get('completion_comment', '').strip()
            req.is_completed = True
            req.completion_date = db.func.now()
            req.completion_comment = completion_comment
            db.session.commit()
            flash("Заявка успешно отмечена как выполненная.", "success")
        return redirect(url_for('repair_request_detail', id=id))

    return render_template('repair_request_detail.html', repair_request=req)
