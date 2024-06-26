from flask import Blueprint
from flask import render_template
from flask_login import current_user

from jiduoduo.models import Testing
from jiduoduo.models import VPS

blueprint = Blueprint('main', __name__, url_prefix='/')


@blueprint.get('/health')
def health():
    return 'ok'


@blueprint.get('/')
def index():
    if current_user.is_authenticated:
        vps_count = VPS.count(
            VPS.user_id == current_user.id,
        )
        testing_count = Testing.count(
            Testing.user_id == current_user.id,
        )
        testing_list = []
    else:
        vps_count = 0
        testing_count = 0
        testing_list = Testing.get_list(
            Testing.is_public == True,
            order_by=[Testing.updated_at.desc()],
            limit=10,
        )

    return render_template(
        'main/index.html',
        vps_count=vps_count,
        testing_count=testing_count,
        testing_list=testing_list
    )
