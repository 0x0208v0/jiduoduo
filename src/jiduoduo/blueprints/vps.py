import logging

from flask import Blueprint
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask_login import current_user
from flask_login import login_required

from jiduoduo.forms.vps import VPSForm
from jiduoduo.models import VPS

logger = logging.getLogger(__name__)

blueprint = Blueprint('vps', __name__)


@blueprint.get('/vps')
@login_required
def list():
    vps_list = VPS.get_list(
        VPS.user_id == current_user.id,
        order_by=[VPS.updated_at.desc()],
    )
    return render_template(
        'vps/list.html',
        vps_list=vps_list,
    )


@blueprint.route('/vps/create', methods=['GET', 'POST'])
@login_required
def create():
    form = VPSForm()
    if request.method == 'POST':
        if not form.validate_on_submit():
            form.flash_errors()

        else:
            vps = VPS(
                user_id=current_user.id,
                name=form.name.data or form.host.data,
                host=form.host.data,
                port=form.port.data,
                user=form.user.data,
                password=form.password.data,
                identify_key=form.identify_key.data,
            )
            vps.save()

            return redirect(url_for('vps.list'))

    return render_template('vps/create.html', form=form)


@blueprint.get('/vps/<string:id>')
@login_required
def detail(id: str):
    vps = VPS.get(id)
    if not vps or vps.user_id != current_user.id:
        return redirect(url_for('vps.list'))

    form = VPSForm(
        name=vps.name,
        host=vps.host,
        port=vps.port,
        user=vps.user,
        password='',
        identify_key='',
    )

    form.password.render_kw['placeholder'] = '已隐藏'
    form.identify_key.render_kw['placeholder'] = '已隐藏'

    return render_template(
        'vps/detail.html',
        vps=vps,
        form=form,
    )


@blueprint.post('/vps/<string:id>')
@login_required
def update(id: str):
    vps = VPS.get(id)
    if not vps or vps.user_id != current_user.id:
        return redirect(url_for('vps.list'))

    form = VPSForm()
    if not form.validate_on_submit():
        form.flash_errors()
        return redirect(url_for('vps.list'))

    vps.name = form.name.data
    vps.host = form.host.data
    vps.port = form.port.data
    vps.user = form.user.data
    vps.password = form.password.data or vps.password
    vps.identify_key = form.identify_key.data or vps.identify_key
    vps.save()

    flash('更新成功', 'success')
    return redirect(url_for('vps.detail', id=id))


@blueprint.route('/vps/<string:id>/delete', methods=['GET', 'POST'])
@login_required
def delete(id: str):
    vps = VPS.get(id)
    if not vps or vps.user_id != current_user.id:
        return redirect(url_for('vps.list'))

    vps.delete()
    flash('VPS已删除', 'success')
    return redirect(url_for('vps.list'))
