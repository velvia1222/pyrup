from wtforms import Form, TextField, IntegerField
from wtforms.validators import Required, Length, NumberRange


class PageForm(Form):
    page_name = TextField('ページ名', validators=[
        Required(),
        Length(min=1, max=64),
        ])
    page_seq = IntegerField('表示順', validators=[
        NumberRange(min=0),
        ])
