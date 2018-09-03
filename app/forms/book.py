from wtforms import Form, StringField, IntegerField
from wtforms.validators import Length, NumberRange, DataRequired, Regexp


#继承wtforms中的Form类 用来为book的search提供验证
class SearchForm(Form):
    q = StringField(validators=[DataRequired(),Length(min=1,max=30)])
    page = IntegerField(validators=[NumberRange(min=1,max=99)],default=1)

class DriftForm(Form):
    recipient_name = StringField(
        validators=[DataRequired(), Length(min=2, max=20, message='收件人姓名长度必须在2到20个字符')])

    mobile = StringField( validators=[DataRequired(),
                                            Regexp('^1[0-9]{10}$', 0, '请输入正确的手机号')])
    message = StringField()
    address = StringField(
        validators=[DataRequired(), Length(min=10, max=70, message='请填写详细地址信息以方便邮寄')])
