#肩负包的初始化代码
from flask import Flask
from app.models.base import db
from flask_login import LoginManager
from flask_mail import Mail

login_manager = LoginManager()
mail = Mail()

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.secure')  #将配置文件写进app中
    app.config.from_object('app.setting')
    #创建时会直接运行

    register_blueprint(app) #将蓝图注册进app中
    db.init_app(app)        #将sqlalchemy对象注册进app
    login_manager.init_app(app) #将登录管理注册进app
    login_manager.login_view='web.login' #确定login界面 实现重定向
    login_manager.login_message='请先登录或注册'#重定向后的提示语句

    mail.init_app(app)

    db.create_all(app=app)#执行创建数据库语句
    return app

def register_blueprint(app):
    #只用一下而临时从book中导入web
    from app.web import web
    #使用app调用flask中的register_blueprint方法将蓝图web注册在app中
    app.register_blueprint(web)