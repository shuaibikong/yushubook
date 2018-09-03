from flask import Blueprint
from flask import render_template

#蓝图的初始化,导入以执行文件中的路由注册

#实例化一个蓝图对象
web = Blueprint('web',__name__)

@web.app_errorhandler(404) #监听状态码为404的异常
def not_found(e):
    #AOP 不要零散的try 而是把所有的异常集中在一起
    return render_template('404.html'), 404

from app.web import book  #这里不会循环调用是因为蓝图注册时已经导入过一次包 所以不会重复读取
from app.web import auth #导入以执行路由注册
from app.web import drift
from app.web import main
from app.web import gift
from app.web import wish
