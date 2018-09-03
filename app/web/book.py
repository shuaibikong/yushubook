from flask_login import current_user

from app.libs.helper import is_isbn_or_key
from app.models.gift import Gift
from app.models.wish import Wish
from app.spider.yushu_book import YuShuBook
from flask import jsonify, request, render_template, flash
import json
from app.view_models.book import BookViewModel, BookCollection
from app.view_models.trade import TradeInfo
from . import web #import __init__中的web可以直接用.
from app.forms.book import SearchForm

#蓝图的方法与app这个flask核心对象的方法基本一致,将蓝图注册进app后可以用蓝图对象直接注册路由
@web.route('/book/search')
def search():
    '''
   q:普通关键字
   page
   '''
    form = SearchForm(request.args) #实例化检验对象来实现校验
    books = BookCollection()   #实例化一个 书籍装饰的集合 对象

    if form.validate(): #校验通过后执行
        q = form.q.data.strip()
        page = form.page.data  #从form中获取q与page来让设定的默认值default生效
        isbn_or_key = is_isbn_or_key(q)
        yushu_book = YuShuBook()

        if isbn_or_key == 'isbn':
            yushu_book.search_by_isbn(q)
            # result = BookViewModel.package_single(result,q)
        else:
            yushu_book.search_by_keyword(q,page)
            # result = BookViewModel.package_collection(result,q)#统一了数据结构

        books.fill(yushu_book,q)
        # return json.dumps(books,default=lambda o: o.__dict__) #dump会用我们后面提供的函数中的方法序列化前面的数据
        # return jsonify(books)

    else:
        #返回一个错误字符串而不是给用户具体错误
        # return jsonify(form.errors)
        flash('搜索的关键字不符合要求,请重新输入关键字')
    return render_template('search_result.html', books=books)

@web.route('/book/<isbn>/detail')
def book_detail(isbn):#显示书籍详细数据
    has_in_gifts = False #既不在心愿清单也不在礼物清单
    has_in_wishes = False
    #取书籍详情数据
    yushu_book = YuShuBook()
    yushu_book.search_by_isbn(isbn)
    book = BookViewModel(yushu_book.first)

    if current_user.is_authenticated: #判断用户是否登录
        if Gift.query.filter_by(uid=current_user.id,isbn=isbn,launched=False).first():
            has_in_gifts = True
        if Wish.query.filter_by(uid=current_user.id,isbn=isbn,launched=False).first():
            has_in_wishes = True

    trade_gift = Gift.query.filter_by(isbn=isbn, launched=False).all() #查出所有赠送者的数据
    trade_wish = Wish.query.filter_by(isbn=isbn, launched=False).all()

    trade_wishes_model = TradeInfo(trade_wish)
    trade_gifts_model = TradeInfo(trade_gift)


    return render_template('book_detail.html',book=book,wishes=trade_wishes_model,gifts=trade_gifts_model,
                           has_in_gifts=has_in_gifts,has_in_wishes=has_in_wishes)


