from wtforms import BooleanField
from wtforms import StringField
from wtforms import SubmitField
from wtforms.validators import DataRequired
from wtforms.validators import Email

from jiduoduo.forms.base import BaseForm


# https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iii-web-forms

class LoginForm(BaseForm):
    email = StringField('邮箱：', validators=[DataRequired(), Email()])
    password = StringField('密码：', validators=[DataRequired()])
    remember_me = BooleanField('保持登录')
    submit = SubmitField('登录')


class RegisterForm(BaseForm):
    email = StringField('邮箱：', validators=[DataRequired(), Email()])
    password = StringField('密码：', validators=[DataRequired()])
    submit = SubmitField('注册')
