import os.path
from app import app, db
from flask import render_template, flash, redirect, url_for, abort, request, send_file
from flask_login import login_user, logout_user, current_user, login_required
from app.forms import LoginForm, EquipmentForm
import sqlalchemy as sa
from app.models import User, Equipment, ComPerson, RepairRequest
from app.qr import generate_qr_code

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
            # if not user.check_password(form.password.data):
            #     flash('Invalid username or password')
            #     return redirect(url_for('login'))
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
@login_required
def add_equipment():
    form = EquipmentForm()
    if form.validate_on_submit():
        equipment = Equipment(
            name=form.name.data,
            territory=form.territory.data,
            office=form.office.data,
            description=form.description.data
        )
        db.session.add(equipment)
        db.session.commit()
        return redirect(f'equipment/{equipment.id}')
    return render_template('add_equipment.html', form=form)


@app.route('/equipment/<int:id>')
def equipment(id):
    equipment = Equipment.query.get_or_404(id)
    return render_template('equipment.html', equipment=equipment)

@app.route('/equipment/<int:id>/delete', methods=['GET', 'POST'])
@login_required
def delete_equipment(id):
    equipment = Equipment.query.get(id)
    equipment.is_deleted = True
    db.session.commit()
    flash('Оборудование успешно удалено!', 'success')
    return redirect(url_for('index'))


@app.route('/equipment/<int:id>/edit', methods=['GET', 'POST'])
@login_required
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
        return redirect(url_for(f'equipment',id=equipment.id))
    else:
        form.name.data = equipment.name
        form.territory.data = equipment.territory
        form.office.data = equipment.office
        form.description.data = equipment.description
        form.submit.label.text = 'Изменить'

    return render_template('add_equipment.html', form=form)


@app.route('/equipment_list')
@login_required
def equipment_list():
    equipments = Equipment.query.filter(Equipment.is_deleted == False).all()
    return render_template('equipment_list2.html', equipments=equipments)


@app.route('/equipment/<int:id>/qr')
@login_required
def equipment_qr(id):
    path = f'..\qrcodes\qr_{id}.png'

    if not os.path.exists(path):
        generate_qr_code(id)

    return send_file(path, mimetype='image/png')

@app.route('/equipment/<int:id>/add_material')
@login_required
def add_material(id):
    pass


@app.route('/equipment/<int:id>/request_repair', methods=['GET', 'POST'])
@login_required
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