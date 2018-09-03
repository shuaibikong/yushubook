from app.libs.httper import HTTP
from flask import current_app

#业务逻辑
class YuShuBook:
    #isbn查询
    #完整的自身的类有职责完成API请求
    #获取数据的API的地址
    isbn_url = 'http://t.yushu.im/v2/book/isbn/{}'#{}是为了方便动态搜索
    keyword_url = 'http://t.yushu.im/v2/book/search?q={}&count={}&start={}'

    def __init__(self):
        self.total = 0
        self.books = []


    def search_by_isbn(self,isbn):
              # 链式查找所以self.isbn_url也可以
        url = self.isbn_url.format(isbn)

        #没有第二个参数则默认为True会收到json格式,在python中json会以dict字典接收
        result = HTTP.get(url)
        self.__fill_single(result) #isbn查询的话一定只会返回一本书,用single单本书籍处理

    def __fill_single(self,data):
        if data:
            self.total = 1
            self.books.append(data) #?

    def __fill_collection(self,data):
        if data:
            self.total = data['total']
            self.books = data['books']

    #关键字查询
    def search_by_keyword(self,keyword,page=1):
        url = self.keyword_url.format(keyword,current_app.config['PER_PAGE'],self.calculate_start(page))
        result = HTTP.get(url)
        self.__fill_collection(result)


    def calculate_start(self,page):
        return (page - 1) * current_app.config['PER_PAGE']

    @property
    def first(self):
        return self.books[0] if self.total >= 1 else None