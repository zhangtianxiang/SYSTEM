from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField,TextAreaField
from wtforms.validators import Required, Length

class QueryForm(FlaskForm):
    select = SelectField('������/���ڲ�ѯ', validators=[Required()], coerce=int,choices=[])
    submit = SubmitField('ȷ��')