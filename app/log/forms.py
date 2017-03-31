from flask_wtf import FlaskForm
from ..models import User
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError,Required, Length, Regexp, EqualTo ,Email

class Unique(object):
    def __init__(self, model, field, message=u'该用户已经存在。'):
        self.model = model
        self.field = field
        self.message = message

    def __call__(self, form, field):
        check = self.model.query.filter(self.field == field.data).first()
        if check:
            raise ValidationError(self.message)

class LoginForm(FlaskForm):
    urpid = StringField('学号', validators=[Required(), Length(11)])
    password = PasswordField('密码', validators=[Required()])
    remember_me = BooleanField('记住密码')
    submit = SubmitField('登陆')

class RegistrationForm(FlaskForm):
    urpid = StringField('学号', validators=[Unique(User,User.urpid),Required(), Length(11)])
    username = StringField('姓名', validators=[Unique(User,User.username),Required(), Length(1, 64) ])
    password = PasswordField('请输入您的密码', validators=[
        Required(), EqualTo('password2', message='密码不匹配！')])
    password2 = PasswordField('请再次输入密码', validators=[Required()])
    submit = SubmitField('注册:-)')

