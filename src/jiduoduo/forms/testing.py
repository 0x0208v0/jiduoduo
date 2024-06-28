from wtforms import SelectField
from wtforms.validators import DataRequired

from jiduoduo.forms.base import BaseForm
from jiduoduo.models.testing import TESTING_TYPE_ZH


class TestingForm(BaseForm):
    type = SelectField(
        '测试类型：',
        choices=[
            (value, label)
            for value, label in TESTING_TYPE_ZH.items()
        ],
        validators=[
            DataRequired(message='测试类型必须选'),
        ],
    )
    vps_id = SelectField(
        'VPS：',
        choices=[
        ],
        validators=[
            DataRequired(message='VPS必填'),
        ],
        render_kw={},
    )
