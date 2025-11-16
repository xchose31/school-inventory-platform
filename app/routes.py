from app import app, db
from flask import render_template, flash, redirect, url_for, abort
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


# @app.route('/edit_equipment/<int:id>', methods=['GET', 'POST'])
# @login_required
# def edit_equipment(id):
#     form = EquipmentForm(current_user.username)
#     equipment = Equipment.query.get(id)
#     if not equipment:
#         abort(404)
#     form.name.data = form.name
#     form.territory.data = form.name
#     form.office.data = form.name
#     form.description.data = form.description
#     if form.validate_on_submit():
#         equipment.name = form.name.data
#         equipment.territory = form.name.data
#         equipment.office = form.name.data
#         equipment.description = form.description.data
#         db.session.commit()
#         flash('Your changes have been saved.')
#         return redirect(url_for('index'))
#
#     return render_template('add_equipment.html', form=form)


# @app.route('/equipment_list')
# @login_required
# def equipment_list():
#     equipments = Equipment.query.all()
#     return render_template('equipment_list.html', equipments=equipments)