from app.models.base import Base, db
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, SmallInteger, func
from sqlalchemy.orm import relationship


from app.spider.yushu_book import YuShuBook


class Wish(Base):
    id = Column(Integer,primary_key=True)
    user = relationship('User') #引用User模型 用user绑定
    uid = Column(Integer,ForeignKey('user.id')) #确定是哪个用户 从user对象中读取属性
    isbn = Column(String(15),nullable=False) #因为没创建数据库 所以用isbn做关联,不能为空但是这里可以重复
    # book = relationship('Book') #引用User模型 用user绑定
    # bid = Column(Integer,ForeignKey('book.id')) #确定是哪个用户 从user对象中读取属性
    launched = Column(Boolean,default=False) #礼物是否送出
    status = Column(SmallInteger,default=1)

    @classmethod
    def get_user_wishes(cls,uid):
        wishes = Wish.query.filter_by(uid=uid, launched=False).order_by(Wish.create_time).all()
        return wishes

    @classmethod
    def get_gifts_count(cls,isbn_list):
        count_list = db.session.query(Gift.isbn,func.count(Gift.id)).filter(
                                      Gift.launched == False,
                                      Gift.status == 1,
                                      Gift.isbn.in_(isbn_list)).group_by(Gift.isbn).all()
        count_list = [{'isbn':w[0],'count':w[1]} for w in count_list]
        return count_list

    @property
    def book(self):
        yushu_book = YuShuBook()
        yushu_book.search_by_isbn(self.isbn)
        return yushu_book.first

from app.models.gift import Gift