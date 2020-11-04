import random
from datetime import datetime

from flask import render_template, request, session, redirect, url_for

from chengse_project import db
from chengse_project.goods.models import Goods
from chengse_project.utils.comment import login_require
from .models import Orders, OrderDetail
from chengse_project.cart.models import Cart
from chengse_project.orders import order_bp
from chengse_project.user.models import Address, Passport


@order_bp.route("/order_page/", methods=["POST"])
@login_require
def show_orders():
    # print(request.form.getlist("cart_id"))
    if request.form.getlist("cart_id"):
        count = None
        cart_list_id = request.form.getlist("cart_id")
        cart_list = Cart.get_cart_list_by_id_list(cart_list_id)
    else:
        count = int(request.form.get("count"))
        # print(count)
        cart_list_id = request.form.getlist("goods_id")
        goods_id = request.form.get("goods_id")
        cart_list = Goods.query.filter_by(id=int(goods_id)).all()

    passport_id = session.get("passport_id")
    addr = Address.query.filter_by(passport_id=passport_id).first()
    addr_all = Address.query.filter_by(passport_id=passport_id).all()
    # print(addr)
    return render_template("h_orders/Orders_confirm1.html", cart_list=cart_list,
                           cart_list_id=cart_list_id, addr=addr, count=count, addr_all=addr_all)


@order_bp.route("/commit_order/", methods=["POST"])
def commit_order():
    passport_id = session.get("passport_id")
    freight = request.form.get("radio")
    addr_id = request.form.get("addr_id")
    goods_id = request.form.getlist("goods_id")
    leave_message = request.form.get("leave_message")
    order_id = datetime.now().strftime('%Y%m%d%H%M%S') + str(random.randint(1000, 10000))
    total_price = request.form.get("goods_price")
    pay_method = request.form.get("radio1")
    goods_actual = request.form.get("actual")
    price_freight = request.form.get("freight")
    goods_count = request.form.getlist("goods_count")
    integral = request.form.get("integral")
    Orders.add_oreder_info(
        order_id=order_id,
        passport_id=passport_id,
        addr_id=addr_id,
        total_count=goods_actual,
        total_price=total_price,
        freight_price=price_freight,
        pay_method=pay_method,
        express=freight,
        leave_message=leave_message
    )
    # print(goods_count)
    # print(goods_id)
    unit_price = request.form.getlist("unit_price")
    for i in range(len(goods_id)):
        # unit_price = request.form.get("unit_price")
        print(unit_price)
        OrderDetail.add_order_detail_info(
            order_id=order_id,
            goods_id=int(goods_id[i]),
            passport_id=passport_id,
            goods_count=int(goods_count[i]),
            goods_price=unit_price[i]
        )
        goods = Goods.query.filter_by(id=int(goods_id[i])).first()
        goods.goods_stock = goods.goods_stock - int(goods_count[i])
        goods.product_sales = goods.product_sales + int(goods_count[i])
        Cart.delete_cart_info(
            passport_id=passport_id,
            goods_id=int(goods_id[i])
        )
    username = session.get("username")
    user = Passport.query.filter_by(username=username).first()
    # print(user)
    user.integral = user.integral + int(integral)
    db.session.add(user)
    db.session.commit()
    return redirect(url_for("order_bp.commit_success", order_id=order_id))


@order_bp.route("/order_detail/<int:order_id>/")
@login_require
def order_detail(order_id):
    passport_id = session.get("passport_id")
    info = Passport.query.filter(Passport.id == passport_id).first()

    goods = OrderDetail.get_goods(order_id)
    addr = Address.query.filter_by(id=goods[0].orders.addr_id).first()
    # print(addr)
    return render_template("h_orders/User_order_detail.html", info=info, goods=goods, addr=addr)


@order_bp.route("/commit_success/<string:order_id>")
def commit_success(order_id):
    passport_id = session.get("passport_id")
    info = Passport.query.filter(Passport.id == passport_id).first()
    return render_template("h_orders/commit_success.html", info=info, order_id=order_id)






