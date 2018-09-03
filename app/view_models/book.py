

class BookViewModel:  #处理单本书籍的书籍信息的类
    def __init__(self,book):
        self.title = book['title']
        self.publisher = book['publisher']
        self.pages = book['pages'] or ''
        self.author = '、'.join(book['author']) #在模板语言中不方便循环所以在这里完成拼接
        self.price =  book['price']
        self.summary = book['summary'] or ''
        self.isbn = book['isbn']
        self.image = book['image']  #如果从API中得到的数据格式不统一则在这里进行裁剪
        self.pubdate = book['pubdate']#出版社
        self.binding = book['binding']#装帧

    @property
    def intro(self):
        intro = filter(lambda x:True if x else False,    #避免 /author //price 的情况出现,将空数据剔除出去并在中间加入'/'
                       [self.author,self.publisher,self.price])
        return '/'.join(intro)

class BookCollection: #用单本书籍的方法来重复处理书籍集合
    def __init__(self):
        self.total = 0 #将页面也要展示的信息进行填充
        self.books = []
        self.keyword = ''

    def fill(self,yushu_book,keyword):
        self.total = yushu_book.total #在yushubook类中对单本的数量和多本的数量进行了区分
        self.books = [BookViewModel(book) for book in yushu_book.books] #将查询到的书籍信息循环放入单本书籍的对象并放进列表中
        self.keyword = keyword



class _BookViewModel:
    @classmethod             #传入原始数据进行处理
    def package_single(cls,data,keyword):
        returned = {
            'books':[],
            'total': 0,
            'keyword': keyword #左上角关键字
        }
        if data:#有数据的话就把total设为1 因为是isbn只有0或1情况
            returned['total'] = 1
            returned['books'] = [cls.__cut_book_data(data)]
        return returned

    @classmethod
    def package_collection(cls,data,keyword):
        returned = {    #数据结构一致
            'books': [],
            'total': 0,
            'keyword': keyword  # 左上角关键字
        }
        if data:
            returned['total'] = data['total']
            returned['books'] = [cls.__cut_book_data(book) for book in data]
        return returned

    @classmethod  #裁剪原始数据
    def __cut_book_data(cls,data):
        book = {
            'title': data['title'],
            'publisher': data['publisher'],
            'pages': data['pages'] or '',
            'author': '、'.join(data['author']),
            'price': data['price'],
            'summary': data['summary'] or '', #空的话就会返回一个''
            'image': data['image']
        }
        return book