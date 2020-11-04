from flask import render_template, request, session, redirect, url_for

from chengse_project import db
from chengse_project.utils.comment import login_require
from .models import Goods, Collect, Browsing
from chengse_project.goods import goods_bp
from .enum import GOODS_TYPE_EN, GOODS_TYPE


@goods_bp.route("/")
def index():
    context = dict()
    for i in range(1, 5):

        goods = Goods.query.filter_by(goods_type_id=i).all()[:8]
        context[f"{GOODS_TYPE_EN[i]}s"] = goods
    # print(context)

    context["hot"] = Goods.query.order_by(Goods.product_sales.desc()).all()[:9]
    context["low"] = Goods.query.order_by(Goods.product_price.desc()).all()[:13]
    context["like"] = Goods.query.order_by(Goods.product_sales.desc()).all()[:8]

    return render_template("h_goods/Home.html", **context)


@goods_bp.route("/goods/<int:goods_id>/")
def goods_detail(goods_id):
    session["goods_id"] = goods_id
    session["url"] = request.url
    passport_id = session.get("passport_id")
    if "is_login" in session:
        Browsing.add_browsing(
            passport_id=passport_id,
            goods_id=goods_id
        )
    collect = Collect.get_collect(goods_id=goods_id)
    # print(collect)
    history = Browsing.query.filter_by(passport_id=passport_id).order_by(Browsing.create_time.desc()).all()[1:4]
    goods = Goods.get_goods_by_id(goods_id=goods_id)
    goods_type = GOODS_TYPE[goods.goods_type_id]
    same_class = Goods.query.filter_by(goods_type_id=goods.goods_type_id).order_by(Goods.product_sales.desc()).all()[:4]
    context = dict(
        goods=goods,
        goods_type=goods_type,
        same_class=same_class,
        collect=collect,
        history=history
    )
    return render_template("h_goods/Product_Detailed.html", **context)


@goods_bp.route("/collect/<int:goods_id>")
@login_require
def collect(goods_id):
    goods_id = session.get("goods_id")
    passport_id = session.get("passport_id")
    Collect.add_collect(passport_id=passport_id, goods_id=goods_id)
    return redirect(url_for("goods_bp.goods_detail", goods_id=goods_id))


@goods_bp.route("/delete/<int:goods_id>/")
def delete(goods_id):
    col = Collect.query.filter_by(goods_id=goods_id).first()
    # print(col)
    db.session.delete(col)
    db.session.commit()
    return redirect(url_for("goods_bp.goods_detail", goods_id=goods_id))


@goods_bp.route("/list/<int:type_id>/<int:index>/")
def all_list(type_id, index):
    low = Goods.query.order_by(Goods.product_price.desc()).all()[:5]
    sort = request.args.get("sort", "default")
    goods = Goods.get_goods_by_type(type_id, sort=sort)
    goods_type_id = type_id
    passport_id = session.get("passport_id")
    history = Browsing.query.filter_by(passport_id=passport_id).order_by(Browsing.create_time.desc()).all()[:3]
    hot = Goods.query.order_by(Goods.product_sales.desc()).all()[:10]
    pagination = Goods.goods_paging(
        goods_type_id=goods_type_id,
        per_page=8,
        sort=sort,
        pindex=index,
    )
    num_pages = range(1, pagination.pages+1)
    # print(history)
    # print(num_pages)
    context = dict(
        pagination=pagination,
        low=low,
        sort=sort,
        goods=goods,
        hot_top1=hot[:1],
        hot=hot[1:10],
        goods_type_id=goods_type_id,
        type_title=GOODS_TYPE[goods_type_id],
        num_pages=num_pages,
        history=history
    )
    return render_template("h_goods/product_list.html", **context)


@goods_bp.route("/search_goods/<int:index>/", methods=["POST", "GET"])
def search(index):
    sort = request.args.get("sort", "default")
    low = Goods.query.order_by(Goods.product_price.desc()).all()[:5]
    hot = Goods.query.order_by(Goods.product_sales.desc()).all()[:10]
    search_text = request.form.get("search")
    if search_text:
        session["search_text"] = search_text
    else:
        search_text = session.get("search_text")
    pagination = Goods.search_list_paging(per_page=4, search_text=search_text, pindex=index, sort=sort)
    # print(pagination.items)
    num_pages = range(1, pagination.pages + 1)
    context = dict(low=low, hot_top1=hot[:1], hot=hot, pagination=pagination, sort=sort, num_pages=num_pages)
    return render_template("h_goods/search_list.html", **context)

