from flask_wtf import FlaskForm
from ..models import Room
from wtforms import StringField, IntegerField, SelectField, SubmitField
from wtforms.validators import Required,Optional, Length, Regexp, EqualTo ,Email

class AgreementForm(FlaskForm):
    days = [(0, ""), (1, "周一"), (2, "周二")]
    times = [(i+1, i + 9) for i in range(14)]
    org = StringField('借用组织', validators=[Required(), Length(1, 64)])
    tel = StringField('联系方式', validators=[Optional(), Length(1, 64)])
    room = SelectField('使用房间', validators=[Required()], coerce=int,choices=[])
    number = IntegerField('使用人数', validators=[Optional()])
    timeday = SelectField('借用日期', validators=[Required()], coerce=int, choices=[])
    fromtime = SelectField('开始时间(24小时制)', validators=[Required()], coerce=int, choices=times)
    totime = SelectField('结束时间(24小时制)', validators=[Required()], coerce=int, choices=times)
    submit = SubmitField('确认')