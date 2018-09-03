from threading import Thread

from flask import current_app,render_template

from app import mail
from flask_mail import Message

def send_aync_email(msg,app):
    with app.app_context():
        try:
            mail.send(msg)
        except Exception as e:
            pass

def send_mail(to, subject, template, **kwargs): #发给谁 邮件标题 邮件内容
    # msg = Message('测试邮件', sender='331009573@qq.com', body='Test',
    #           recipients=['331009573@qq.com'])
    msg = Message('[鱼书]' + ' ' + subject,
                  sender=current_app.config['MAIL_USERNAME'],
                  recipients=[to])
    msg.html = render_template(template,**kwargs)
    app = current_app._get_current_object()
    thr = Thread(target=send_aync_email, args=[msg,app])
    thr.start()