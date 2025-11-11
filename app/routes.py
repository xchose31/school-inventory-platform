from app import app, db
from flask import render_template, flash, redirect, url_for
from flask_login import login_user, logout_user, current_user, login_required
from app.forms import LoginForm
import sqlalchemy as sa
from app.models import User

@app.route('/')
def index():
    return render_template('base.html')

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

@login_required
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))