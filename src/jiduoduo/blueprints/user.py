from flask import Blueprint
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask_login import current_user
from flask_login import login_required
from flask_login import login_user
from flask_login import logout_user

from jiduoduo.forms.user import LoginForm
from jiduoduo.forms.user import RegisterForm
from jiduoduo.models import User

blueprint = Blueprint('user', __name__, url_prefix='/')


@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            try:
                user = User.login(email=form.email.data, password=form.password.data)
                login_user(user, remember=form.remember_me.data)
                return redirect(url_for('main.index'))
            except ValueError as e:
                flash(f'{e}', 'error')
        else:
            form.flash_errors()
    return render_template('user/login.html', form=form)


@blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            try:
                User.register(email=form.email.data, password=form.password.data)
                flash('注册成功！', 'success')
                return redirect(url_for('user.login'))
            except ValueError as e:
                flash(f'{e}', 'error')
        else:
            form.flash_errors()
    return render_template('user/register.html', form=form)


@blueprint.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@blueprint.route('/delete', methods=['GET', 'POST'])
@login_required
def delete():
    current_user.delete()
    flash('账户已删除', 'success')
    return redirect(url_for('main.index'))


@blueprint.route('/setting', methods=['GET', 'POST'])
@login_required
def setting():
    return render_template('user/setting.html')
