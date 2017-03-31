from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField,TextAreaField
from wtforms.validators import Required, Length

class QueryForm(FlaskForm):
    select = SelectField('按房间/日期查询', validators=[Required()], coerce=int,choices=[])
    submit = SubmitField('确认')
