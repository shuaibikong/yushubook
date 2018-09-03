#开启调试模式
#配置文件函数必须大写来覆盖原本默认存在的配置
#密码等机密的信息放入secure
DEBUG = True
SQLALCHEMY_DATABASE_URI = 'mysql+cymysql://root:123456@localhost:3306/fisher'
SECRET_KEY ='\x88D\xf09\x91\x07\x98\x89\x87\x96\xa0A\xc68'

#Email配置
MAIL_SERVER = 'smtp.qq.com' #电子邮件服务器 采用公开的qq电子邮箱服务器
MAIL_PORT = 465 #qq邮箱对应的端口
MAIL_USE_SSL = True #qq使用的协议为SSL
MAIL_USE_TSL = False
MAIL_USERNAME = '331009573@qq.com' #自己的邮箱地址
MAIL_PASSWORD = 'omnncthfmdosbhfi'    #邮箱-->设置-->账号中获得的密码

