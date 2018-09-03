from datetime import datetime

from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy, BaseQuery
from sqlalchemy import Column, Integer, String,Boolean,ForeignKey,SmallInteger
from contextlib import contextmanager

class SQLAlchemy(_SQLAlchemy):
    @contextmanager
    def auto_commit(self):
        try:
            yield
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e

class Query(BaseQuery):
    def filter_by(self, **kwargs):
        if 'status' not in kwargs.keys():
            kwargs['status'] = 1
        return super(Query,self).filter_by(**kwargs)

db = SQLAlchemy(query_class=Query)

#所有模型共有的属性
class Base(db.Model): #让子模型直接继承Bsae间接继承了db.model
    __abstract__ = True
    # create_time = Column('create_time',Integer)
    create_time = Column('create_time',Integer) #数字类型的时间戳 需要在下面转换
    status = Column(SmallInteger,default=1)#是否软删除

    def __init__(self): #记录生成时间 实例化时自动生成一个时间戳
        self.create_time = int(datetime.now().timestamp())

    def set_attrs(self,attrs_dict): #接收一个字典参数,如果键和模型属性相同,就把值赋给模型相关属性
        for key ,value in attrs_dict.items(): #获取字典的键值对 并赋值给两个变量
            if hasattr(self,key) and key != 'id': #判断 self中是否有key这个属性 , 如果的话就赋值
                setattr(self,key,value)  #hasattr 判断是否有属性 setattr 给属性赋值

    @property
    def create_datetime(self):
        if self.create_time:
            return datetime.fromtimestamp(self.create_time) #将时间戳转化为时间类型
        else:
            return None

    def delete(self):
        self.status = 0
