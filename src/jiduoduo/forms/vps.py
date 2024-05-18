from wtforms import IntegerField
from wtforms import StringField
from wtforms import TextAreaField
from wtforms.validators import DataRequired
from wtforms.validators import ValidationError

from jiduoduo.forms.base import BaseForm


def max_choices(value=4):
    message = f'You cannot select more than {value} options.'

    def _max_choices(form, field):
        if len(field.data) > value:
            raise ValidationError(message)

    return _max_choices


class VPSForm(BaseForm):
    host = StringField(
        'VPS 地址：',
        validators=[
            DataRequired(message='VPS地址必填'),
        ],
        render_kw={
            'placeholder': '如：231.3.43.85',
        }
    )
    name = StringField(
        'VPS 名称：',
        render_kw={
            'placeholder': '如：斯巴达36刀建站鸡；可以不填，默认为VPS地址',
        }
    )
    port = IntegerField(
        'SSH 端口：',
        default=22,
        validators=[
            DataRequired(message='SSH端口必填'),
        ],
        render_kw={
            'placeholder': '如：22 或者 其他自定义端口',
        }
    )
    user = StringField(
        'SSH 用户：',
        default='root',
        validators=[
            DataRequired(message='SSH用户必填'),
        ],
        render_kw={
            'placeholder': '如：root 或者 ubuntu 或者 别的',
        }
    )
    password = StringField(
        'SSH 密码：',
        render_kw={
            'placeholder': '和登陆Key二选一，填一个就行',
        }
    )
    identify_key = TextAreaField(
        'SSH Key：',
        render_kw={
            'rows': 5,
            'placeholder': '和登陆密码二选一，填一个就行',
        }

    )

    def validate(self, extra_validators=None) -> bool:
        result = super().validate(extra_validators=extra_validators)

        if not self.password.data and not self.identify_key.data:
            self.password.errors.append('和登陆Key二选一')
            self.identify_key.errors.append('和登陆密码二选一')
            result = False

        return result
