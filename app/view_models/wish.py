from app.view_models.book import BookViewModel


class MyWishes:
    def __init__(self,wish_of_mine, wish_count_list):
        self.wishes = []
        self.__wish_of_mine = wish_of_mine
        self.__wish_count_list = wish_count_list

        self.wishes = self.__parse()


    def __parse(self):
        temp_wishes = []
        for wish in self.__wish_of_mine:
            my_gift = self.__matching(wish)
            temp_wishes.append(my_gift)
        return temp_wishes

    def __matching(self,wish):
        count = 0
        for wish_count in self.__wish_count_list:
            if wish_count['isbn'] == wish.isbn:
                count = wish_count['count']
        r = {
            'id': wish.id,
            'gifts-count': count,
            'book': BookViewModel(wish.book)
            }

        return r