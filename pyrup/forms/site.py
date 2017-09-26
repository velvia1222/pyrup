from wtforms import Form, TextField, IntegerField
from wtforms.validators import Required, Length, NumberRange


class SiteForm(Form):
    site_name = TextField('サイト名', validators=[
        Required(),
        Length(min=1, max=64),
        ])
    site_seq = IntegerField('表示順', validators=[
        NumberRange(min=0, max=999999999),
        ])
