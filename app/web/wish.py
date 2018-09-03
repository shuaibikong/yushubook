from app.models.wish import Wish
from app.view_models.trade import MyTrades
from app.view_models.wish import MyWishes
from . import web
from app.models.base import db
from flask import current_app, flash, redirect,url_for,render_template
from flask_login import current_user, login_required


@web.route('/my/wish')
@login_required
def my_wish():
    uid = current_user.id
    wishes_of_mine = Wish.get_user_wishes(uid)
    isbn_list = [wish.isbn for wish in wishes_of_mine]
    gift_count_list = Wish.get_gifts_count(isbn_list)
    view_model = MyTrades(wishes_of_mine, gift_count_list)
    return render_template('my_wish.html',wishes=view_model.trades)


@web.route('/wish/book/<isbn>')
@login_required
def save_to_wish(isbn):
    if current_user.can_save_to_list(isbn):
        with db.auto_commit():
            wish = Wish()
            wish.uid = current_user.id
            wish.isbn = isbn
            db.session.add(wish)
    else:
        flash('这本书已经在您的心愿清单了')
    return redirect(url_for('web.book_detail',isbn=isbn))

@web.route('/redraw_from_wish')
def redraw_from_wish():
    pass
