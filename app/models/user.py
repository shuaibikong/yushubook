from math import floor

from flask import current_app

from app.libs.enum import PendingStatus
from app.libs.helper import is_isbn_or_key
from app.models.base import Base, db
from sqlalchemy import Column, Integer, String,Boolean,Float
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from app import login_manager
from app.models.drift import Drift
from app.models.gift import Gift
from app.models.wish import Wish
from app.spider.yushu_book import YuShuBook
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


class User(Base,UserMixin):
    id = Column(Integer,primary_key=True)
    nickname = Column(String(24),nullable=False)
    phone_number = Column(String(18),unique=True)
    _password = Column('password',String(128),nullable=False)
    email = Column(String(50),unique=True,nullable=False)
    confirmed = Column(Boolean,default=False)
    beans = Column(Float,default=0)   #鱼豆数量,积分
    send_counter = Column(Integer,default=0)
    receive_counter = Column(Integer,default=0)
    wx_open_id = Column(String(50))
    wx_name = Column(String(32))

    @property  # 可以像查看属性一样查看一个方法
    def password(self):
        return self._password

    @password.setter  # 可以向password写入数据
    def password(self, raw):  # 原始密码
        self._password = generate_password_hash(raw) #将加密后的原始密码赋值给password

    def check_password(self,raw): #将登录时输入的 未加密 密码加密后与数据库中密码比对
        return check_password_hash(self._password,raw)

    def can_save_to_list(self,isbn):
        #如果不是isbn
        if is_isbn_or_key(isbn) != 'isbn':
            return False
        yushu_book = YuShuBook()
        yushu_book.search_by_isbn(isbn)
        if not yushu_book.first: #如果没有从api中查询到
            return False
        #不允许一个用户同时赠送多本相同的图书
        #一个用户不可能同时成为赠送者和索要者

        #既不在心愿清单中 也不能在赠送清单
        gifting = Gift.query.filter_by(uid=self.id,isbn=isbn,
                                    launched=False).first()
        wishing = Wish.query.filter_by(uid=self.id,isbn=isbn,
                                       launched=False).first()

        if not gifting and not wishing:
            return True
        else:
            return False

    def generate_token(self, expiration=600): #生成一个token记录用户id号 加密
        s = Serializer(current_app.config['SECRET_KEY'],expiration)
        temp = s.dumps({'id': self.id}).decode()
        return temp

    @staticmethod
    def reset_password(new_password,token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        uid = data.get('id')
        with db.auto_commit():
            user = User.query.get(uid)
            user.password = new_password
        return True

    def can_send_drift(self):
        if self.beans < 1:
            return False
        success_gifts_count = Gift.query.filter_by(uid=self.id, launched=True).count()
        success_receive_count = Drift.query.filter_by(requester_id=self.id, pending=PendingStatus.Success).count()

        return True if \
            floor(success_receive_count / 2)  <= floor(success_gifts_count) \
            else False

    @property
    def summary(self):
        return dict(
            nickname = self.nickname,
            beans = self.beans,
            email = self.email,
            send_receive = str(self.send_counter) + '/' + str(self.receive_counter)
        )




@login_manager.user_loader
def get_user(uid):  #通过uid号来返回对应的用户模型,uid数值的传入由flask_login读取cookie获取
    return User.query.get(int(uid))