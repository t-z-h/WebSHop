from flask import render_template, request, session, jsonify, redirect, url_for
from sqlalchemy import func

from chengse_project import db
from chengse_project.goods.models import Goods
from chengse_project.utils.comment import login_require
from . import cart_bp
from .models import Cart


@cart_bp.route("/show_cart/")
@login_require
def show_cart():
    session["url"] = request.url
    recommend = Goods.query.order_by(Goods.product_sales.desc()).all()[:6]
    passport_id = session.get("passport_id")
    cart_list = db.session.query(Goods, Cart).filter(Cart.passport_id == passport_id, Goods.id == Cart.goods_id).all()
    print(cart_list)
    return render_template("h_carts/Shop_cart.html", cart_list=cart_list, Cart=Cart, recommend=recommend)


@cart_bp.route("/add/")
def add_cart():
    goods_id = request.args.get("goods_id")
    goods_count = request.args.get("goods_count")
    goods_count = int(goods_count)
    passport_id = session.get("passport_id")

    # print(goods_id, goods_count, passport_id)
    res = Cart.add_one_cart_info(
        passport_id=passport_id,
        goods_id=goods_id,
        goods_count=goods_count
    )
    # print(res)
    return jsonify(res="true" if res else "false")


@cart_bp.route("/count/")
def count():
    passport_id = session.get("passport_id")
    res = db.session.query(func.sum(Cart.goods_count)).filter_by(passport_id=passport_id).first()[0]
    if res:
        return jsonify(res=int(res))
    else:
        return jsonify(res=0)


@cart_bp.route("/update/")
def cart_update():
    goods_id = request.args.get("goods_id")
    goods_count = request.args.get("goods_count")
    passport_id = session.get("passport_id")
    res = Cart.update_one_cart_info(
        passport_id=passport_id,
        goods_id=goods_id,
        goods_count=int(goods_count)
    )
    if res:
        return jsonify(res=1)
    else:
        return jsonify(res=0)


@cart_bp.route("/delete_goods/")
def delete_goods():

    passport_id = session.get("passport_id")
    goods_id = request.args.get("goods_id")
    res = Cart.delete_cart_info(
        passport_id=passport_id,
        goods_id=goods_id
    )
    if res:
        return jsonify(res="success")
    else:
        return jsonify(res=0)










