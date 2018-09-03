from flask import current_app

from app.models.base import Base, db
from sqlalchemy import Column, Integer, String,Boolean,ForeignKey,SmallInteger,desc,func
from sqlalchemy.orm import relationship
from collections import namedtuple

from app.spider.yushu_book import YuShuBook


class Gift(Base):
    id = Column(Integer,primary_key=True)
    user = relationship('User') #引用User模型 用user绑定 用来读取用户信息
    uid = Column(Integer,ForeignKey('user.id')) #确定是哪个用户 从user对象中读取属性
    isbn = Column(String(15),nullable=False) #因为没创建数据库 所以用isbn做关联,不能为空但是这里可以重复

    # book = relationship('Book') #引用User模型 用user绑定
    # bid = Column(Integer,ForeignKey('book.id')) #确定是哪个用户 从user对象中读取属性
    launched = Column(Boolean,default=False) #礼物是否送出
    status = Column(SmallInteger,default=1)

    #类代表礼物这个事物,是抽象的 最近的礼物不该属于某一个礼物
    @classmethod
    def recent(cls): #最近的礼物
        #链式调用
        recent_gift = Gift.query.filter_by(launched=False).group_by(Gift.isbn).order_by(
            desc(Gift.create_time)).distinct().limit(current_app.config['RECENT_BOOK_COUNT']
                                    ).all() #没有赠送的礼物
        return recent_gift


    @property
    def book(self):
        yushu_book = YuShuBook()
        yushu_book.search_by_isbn(self.isbn)
        return yushu_book.first

    @classmethod
    def get_user_gifts(cls,uid):
        gifts = Gift.query.filter_by(uid=uid,launched=False).order_by(
            desc(Gift.create_time)).all()
        return gifts

    @classmethod
    def get_wish_count(cls,isbn_list):
        count_list = db.session.query(func.count(Wish.id),Wish.isbn).filter(Wish.launched == False,
                                      Wish.isbn.in_(isbn_list),
                                      Wish.status == 1).group_by(
            Wish.isbn).all()
        count_list = [{'isbn':w[1],'count':w[0]} for w in count_list]
        return count_list

    def is_yourself_gift(self, uid):
        return True if self.uid == uid else False

from app.models.wish import Wish
