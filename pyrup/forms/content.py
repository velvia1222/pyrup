from wtforms import (
        Form,
        TextAreaField,
        FileField,
        IntegerField,
        )
from wtforms.validators import NumberRange


class ContentForm(Form):
    content_text = TextAreaField('テキスト')
    image_file = FileField('画像ファイル')
    attach_file = FileField('添付ファイル')
    content_seq = IntegerField('表示順', validators=[
        NumberRange(min=0),
        ])
