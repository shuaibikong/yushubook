from sqlalchemy import Column, Integer, String
from app.models.base import Base


class Book(Base):
    id = Column(Integer,primary_key=True,autoincrement=True)#书籍的id
    title = Column(String(50),nullable=False) #书名
    author = Column(String(30),default='未名') #作者
    binding = Column(String(20))  # 是否精装
    publisher = Column(String(50))#出版社
    price = Column(String(20))
    pages = Column(Integer)
    pubdate = Column(String(20))  #出版年月
    isbn = Column(String(15),nullable=False,unique=True)#unique唯一索引让数据不重复
    summary = Column(String(1000))#书籍简介
    image = Column(String(50))

