from app import app, db
from flask import render_template, flash, redirect, url_for, abort, request
from flask_login import login_user, logout_user, current_user, login_required
from app.forms import LoginForm, EquipmentForm
import sqlalchemy as sa
from app.models import User, Equipment

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

@app.route('/delete_equipment/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_equipment(id):
    equipment = Equipment.query.get(id)
    db.session.delete(equipment)
    db.session.commit()
    flash('Оборудование успешно удалено!', 'success')
    return redirect(url_for('index'))


@app.route('/edit_equipment/<int:id>', methods=['GET', 'POST'])
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
    equipments = Equipment.query.all()
    return render_template('equipment_list2.html', equipments=equipments)