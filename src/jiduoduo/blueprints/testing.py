import logging

from flask import Blueprint
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask_login import current_user
from flask_login import login_required

from jiduoduo.forms.testing import TestingForm
from jiduoduo.models import Testing
from jiduoduo.models import VPS
from jiduoduo.tasks import run_testing

logger = logging.getLogger(__name__)

blueprint = Blueprint('testing', __name__)


@blueprint.get('/testing')
@login_required
def list():
    testing_list = Testing.get_list(
        Testing.user_id == current_user.id,
        order_by=[Testing.updated_at.desc()],
    )
    return render_template(
        'testing/list.html',
        testing_list=testing_list,
    )


@blueprint.route('/testing/create', methods=['GET', 'POST'])
@login_required
def create():
    type = request.args.get('type') or request.form.get('type')
    vps_id = request.args.get('vps_id') or request.form.get('vps_id')

    form = TestingForm(
        type=type,
        vps_id=vps_id,
    )
    form.vps_id.choices = [
        (str(id), name)
        for id, name in VPS.get_id_name_list(
            VPS.user_id == current_user.id
        )
    ]

    if request.method == 'POST':
        vps = VPS.get(vps_id)
        if not vps or vps.user_id != current_user.id:
            flash(f'VPS不存在, id={vps_id}', 'error')

        if not form.validate_on_submit():
            form.flash_errors()

        else:
            testing = Testing.create(type=type, vps_or_id=vps, user_or_id=current_user)
            run_testing.delay(testing_id=testing.id)
            return redirect(url_for('testing.detail', id=testing.id))

    return render_template('testing/create.html', form=form)


@blueprint.get('/testing/<string:id>')
@login_required
def detail(id: str):
    testing = Testing.get(id)
    if not testing or testing.user_id != current_user.id:
        return redirect(url_for('testing.list'))

    return render_template(
        'testing/detail.html',
        testing=testing,
    )


@blueprint.route('/testing/<string:id>/rerun', methods=['GET', 'POST'])
def rerun(id: str):
    testing = Testing.get(id)
    if not testing or testing.user_id != current_user.id:
        return redirect(url_for('testing.list'))

    testing.set_state_created()
    run_testing.delay(testing_id=testing.id)

    return redirect(url_for('testing.detail', id=id))


@blueprint.route('/testing/<string:id>/delete', methods=['GET', 'POST'])
@login_required
def delete(id: str):
    testing = Testing.get(id)
    if not testing or testing.user_id != current_user.id:
        return redirect(url_for('testing.list'))

    testing.delete()
    flash('VPS已删除', 'success')
    return redirect(url_for('testing.list'))
