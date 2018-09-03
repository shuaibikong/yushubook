from wtforms import Form,StringField,IntegerField,PasswordField
from wtforms.validators import Length, NumberRange, DataRequired, Email, ValidationError, EqualTo

from app.models.user import User


class RegisterForm(Form):
    email = StringField(validators=[DataRequired(),Length(8,64),Email(message='电子邮件不符合规范')]) #Email验证器 验证邮件格式
    password = PasswordField(validators=[DataRequired(message='密码不可为空'),Length(6,32)])
    nickname = StringField(validators=[DataRequired(),Length(2,10,message='昵称为2-10个字符')])

    def validate_email(self,field):
        if User.query.filter_by(email=field.data).first(): #数据库查询 根据field.data获取相应的数据   .first()只获取查询到的第一个数据
            raise ValidationError('电子邮件已经被注册')#填入验证失败后要返回给用户的错误原因

    def validate_nickname(self,field):#field由wtforms传入 field.data为需要的数据
        if User.query.filter_by(nickname=field.data).first():
            raise ValidationError('昵称已存在')

class LoginForm(Form):
    email = StringField(validators=[DataRequired(),Length(8,64),Email(message='邮箱格式不合法')])
    password = PasswordField(validators=[DataRequired(message='密码不可为空'),Length(6,32)])

class EmailForm(Form):
    email = StringField(validators=[DataRequired(),Length(8,64),Email(message='电子邮件不符合规范')])

class ResetPasswordForm(Form):
    password1 = PasswordField(validators=[DataRequired(),
                                          Length(6,32,message='密码长度为6到20个字符'),
                                          EqualTo('password2',message='两次输入的密码不同')])
    password2 = PasswordField(validators=[DataRequired(),Length(6,32)])