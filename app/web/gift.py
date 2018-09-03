from flask import request, current_app, flash, redirect, url_for,render_template

from app.libs.enum import PendingStatus
from app.models.base import db
from app.models.drift import Drift
from app.models.gift import Gift
from app.view_models.gift import MyGifts
from app.view_models.trade import MyTrades
from . import web
from flask_login import login_required,current_user

@web.route('/my/gifts')
@login_required #需要一个get_uid方法 在User模型中方便拿到数据
def my_gifts():
    uid = current_user.id
    gifts_of_mine = Gift.get_user_gifts(uid)
    isbn_list = [gift.isbn for gift in gifts_of_mine]
    wish_count_list = Gift.get_wish_count(isbn_list)
    view_model = MyTrades(gifts_of_mine,wish_count_list)
    return render_template('my_gifts.html',gifts=view_model.trades)

@web.route('/gifts/book/<isbn>')
@login_required
def save_to_gifts(isbn):
    if current_user.can_save_to_list(isbn): #判断能否存入赠送清单
        with db.auto_commit():
            gift = Gift()
            gift.isbn = isbn
            gift.uid = current_user.id #一个实例化后的User的模型,通过模型中的get_user来转化为一个模型
            current_user.beans += current_app.config['BEANS_UPLOAD_ONE_BOOK']
            db.session.add(gift)
    else:
        flash('这本书已经在你的心愿清单了')
    return redirect(url_for('web.book_detail',isbn=isbn)) #赠送成功后重定向到当前书籍页面


@web.route('/gifts/<gid>/redraw')
@login_required
def redraw_from_gifts(gid):
    gift = Gift.query.filter_by(id=gid, launched=False).first_or_404()
    drift = Drift.query.filter_by(gift_id=gift.id, pending=PendingStatus.Waiting).fitst()
    if drift:
        flash('这个礼物正处于交易状态,请先完成该交易')
        return redirect(url_for('web.pending'))
    else:
        with db.auto_commit():
            current_user.beans -= current_app.conifg['BEANS_UPLOAD_ONE_BOOK']
            gift.delete()
        return redirect(url_for('web.my_gifts'))