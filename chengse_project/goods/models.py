from datetime import datetime

from sqlalchemy import func

from chengse_project import db
from chengse_project.base_model.base_model import BaseModel


class Goods(BaseModel):
    __tablename__ = "s_goods"
    goods_type_id = db.Column(db.SmallInteger)  # 商品类型id
    product_title = db.Column(db.String(50), nullable=False)  # 产品名称
    product_subhead = db.Column(db.String(200), default="无")  # 产品副标题
    product_price = db.Column(db.DECIMAL(10, 2), nullable=False)  # 产品价格
    index_image = db.Column(db.String(60))  # 首页商品图片
    product_original = db.Column(db.DECIMAL(10, 2))  # 原价
    product_sales = db.Column(db.Integer, default=0)  # 产品销量
    product_image = db.Column(db.String(60))  # 产品图片
    goods_stock = db.Column(db.Integer, default=0)  # 商品库存
    product_weight = db.Column(db.Integer, default=0)  # 产品重量
    detail_image = db.Column(db.String(60))  # 详情图片
    detail_parameter = db.Column(db.Text)  # 产品参数
    colt = db.relationship("Collect", backref="col_goods")
    carts = db.relationship("Cart", backref="goods")
    order = db.relationship("OrderDetail", backref="order_goods")
    browsing = db.relationship("Browsing", backref="browsing_goods")

    @classmethod
    def get_goods_by_id(cls, goods_id):
        goods = Goods.query.get(goods_id)
        return goods

    @classmethod
    def get_goods_by_type(cls, goods_type_id, limit=None, sort="default"):
        """根据商品类型id查询商品信息"""
        from chengse_project.goods.enum import sort_map
        goods_list = cls.query.filter_by(goods_type_id=goods_type_id).order_by(sort_map[sort].desc()).all()
        # goods_list = cls.query.filter_by(goods_type_id=goods_type_id).all()
        if limit:
            goods_list = goods_list[:limit]
        return goods_list

    @classmethod
    def goods_paging(cls, goods_type_id, per_page, pindex=1, sort="default"):
        from chengse_project.goods.enum import sort_map
        pagination = Goods.query.filter_by(goods_type_id=goods_type_id).order_by(sort_map[sort].desc()).paginate(
            page=pindex,
            per_page=per_page,
            error_out=False
        )
        return pagination

    @classmethod
    def search_list_paging(cls, search_text, per_page, pindex=1, sort="default"):
        from chengse_project.goods.enum import sort_map
        # print(db.session.query(Goods).filter(Goods.product_title.like(f"%{search_text}%")).order_by(sort_map[sort].desc()).all())
        pagination = db.session.query(Goods).filter(Goods.product_title.like(f"%{search_text}%")).order_by(
            sort_map[sort].desc()).paginate(
            page=pindex,
            per_page=per_page,
            error_out=False
        )
        # print(pagination)
        return pagination


class Collect(BaseModel):
    __tablename__ = "collect"
    passport_id = db.Column(db.Integer, db.ForeignKey("s_user_account.id"), nullable=False)
    goods_id = db.Column(db.Integer, db.ForeignKey("s_goods.id"), nullable=False)
    goods_count = db.Column(db.Integer, default=1)

    @classmethod
    def get_collect(cls, goods_id):
        obj = Collect.query.filter_by(goods_id=goods_id).first()
        # print(obj)
        return obj

    @classmethod
    def add_collect(cls, passport_id, goods_id):
        collect = Collect(
            passport_id=passport_id,
            goods_id=goods_id
        )
        db.session.add(collect)
        db.session.commit()
        return True


class Browsing(BaseModel):
    __tablename__ = "browsing_history"
    passport_id = db.Column(db.Integer, db.ForeignKey("s_user_account.id"), nullable=False)
    goods_id = db.Column(db.Integer, db.ForeignKey("s_goods.id"), nullable=False)

    @classmethod
    def add_browsing(cls, passport_id, goods_id):
        browsing = Browsing(
            passport_id=passport_id,
            goods_id=goods_id
        )
        db.session.add(browsing)
        db.session.commit()
