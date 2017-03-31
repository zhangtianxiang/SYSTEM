from flask import flash
from flask_wtf import FlaskForm
from ..models import Room,Agreement
from wtforms import StringField, IntegerField, SelectField, SubmitField
from wtforms.validators import ValidationError,Required,Optional, Length

class CheckTime(object):
    def __init__(self,message=u'时间冲突'):
        self.message = message

    def __call__(self, form, field):
        room_id = form.room.data
        timeday=form.timeday.choices[form.timeday.data-1][1]
        fromtime=form.fromtime.choices[form.fromtime.data-1][1]
        totime=form.totime.choices[form.totime.data-1][1]
        #筛选同一天，同一房间的借用
        agr = Agreement.query.filter(Agreement.timeday == timeday).filter(Agreement.room_id == room_id).all()
        # 检查时间是否倒置
        check = True if fromtime>=totime else False
        # 检查时间冲突
        for each in agr:
            if (each.fromtime>=fromtime and each.fromtime<=totime)\
                or (each.totime>=fromtime and each.totime<=totime):
                    check = True
        if check:
            flash("借用失败，请检查房间和时间！")
            raise ValidationError(self.message)

class AgreementForm(FlaskForm):
    days = [(0, ""), (1, "周一"), (2, "周二")]
    times = [(i+1, i + 9) for i in range(14)]
    org = StringField('借用组织', validators=[Required(), Length(1, 64)])
    tel = StringField('联系方式', validators=[Optional(), Length(1, 64)])
    room = SelectField('使用房间', validators=[Required()], coerce=int,choices=[])
    number = IntegerField('使用人数', validators=[Optional()])
    timeday = SelectField('借用日期', validators=[Required()], coerce=int, choices=[])
    fromtime = SelectField('开始时间(24小时制)', validators=[Required()], coerce=int, choices=times)
    totime = SelectField('结束时间(24小时制)', validators=[CheckTime(),Required()], coerce=int, choices=times)
    submit = SubmitField('确认')