from app.libs.email import send_mail
from app.models.base import db
from app.models.user import User
from . import web
from flask import render_template, request, redirect, url_for, make_response, flash
from app.forms.auth import RegisterForm, LoginForm, EmailForm, ResetPasswordForm
from flask_login import login_user, logout_user


@web.route('/register',methods=['GET','POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate(): #request.method根据http请求状态来判断是获取页面还是提交页面
        with db.auto_commit():
            user = User()
            user.set_attrs(form.data) #form.data 验证后的用户提交信息 格式为字典
            db.session.add(user) #在数据库中添加一条记录
            return redirect(url_for('web.login'))#注册成功后重定向到登录页面
    return render_template('auth/register.html',form=form)


@web.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm(request.form)  #request.form获取提交过来的表单信息
    if  request.method == 'POST' and form.validate():
        user = User.query.filter_by(email=form.email.data).first()#查询是否存在提交的用户
        if user and user.check_password(form.password.data):
            login_user(user) #使用login_user需要在User模型中继承UserMixin 用来将票据存入cookie
            next = request.args.get('next') #request.args可以获取url中? 后面的参数 从没有权限访问的页面跳转过来会自带next
            if not next or not next.startswith('/'):
                next = url_for('web.index')
            return redirect(next)

        else:
            flash('账号不存在或密码错误')
    return render_template('auth/login.html',form=form)

@web.route('/register/password',methods=['GET','POST'])
def forget_password_request():
    form = EmailForm(request.form)
    if request.method == 'POST':
        if form.validate():
            account_email = form.email.data
            user = User.query.filter_by(email=account_email).first_or_404()
            send_mail(form.email.data,'重置你的密码',
                      'email/reset_password.html',user=user,token=user.generate_token())
            flash('一封邮件已经发送到您的邮箱' + account_email + ',请及时查收')
    return render_template('auth/forget_password_request.html', form=form)

@web.route('/reset/password/<token>',methods=['GET','POST'])
def forget_password(token):
    form = ResetPasswordForm(request.form)
    if request.method == 'POST' and form.validate():
        success = User.reset_password(form.password1.data,token)
        if success:
            flash('您的密码已经成功找回,请使用新密码登录')
            return redirect(url_for('web.login'))
        else:
            flash('密码重置失败')
    return render_template('auth/forget_password.html',form=form)

@web.route('/change/password',methods=['GET','POST'])
def change_password():
    pass

@web.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('web.index'))