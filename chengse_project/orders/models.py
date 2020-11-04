from chengse_project import db
from chengse_project.base_model.base_model import BaseModel, Base


class Orders(Base):
    __tablename__ = "orders"
    order_id = db.Column(db.String(64), primary_key=True)
    passport_id = db.Column(db.Integer, db.ForeignKey('s_user_account.id'), nullable=False)
    addr_id = db.Column(db.Integer, db.ForeignKey("s_user_address.id"), nullable=False)
    total_count = db.Column(db.Integer, default=1)
    total_price = db.Column(db.DECIMAL(10, 2))
    freight_price = db.Column(db.DECIMAL(10, 2))   # 商品运费
    pay_method = db.Column(db.String(10), default="余额支付")
    order_status = db.Column(db.String(10), default="待发货")
    express = db.Column(db.String(10), default="中通快递")      # 快递方式
    leave_message = db.Column(db.String(60))  # 留言
    order_details = db.relationship("OrderDetail", backref="orders")

    @classmethod
    def add_oreder_info(cls, order_id, passport_id, addr_id, total_count, total_price, freight_price, pay_method, express, leave_message):
        info = cls(
            order_id=order_id,
            passport_id=passport_id,
            addr_id=addr_id,
            total_count=total_count,
            total_price=total_price,
            freight_price=freight_price,
            pay_method=pay_method,
            express=express,
            leave_message=leave_message
        )
        db.session.add(info)
        db.session.commit()

    @classmethod
    def search_orders_all(cls, passport_id):
        orders = cls.query.filter_by(passport_id=passport_id).all()
        return orders


class OrderDetail(BaseModel):
    __tablename__ = "order_detail"
    order_id = db.Column(db.String(64), db.ForeignKey('orders.order_id'), nullable=False)
    goods_id = db.Column(db.Integer, db.ForeignKey("s_goods.id"), nullable=False)
    passport_id = db.Column(db.Integer, db.ForeignKey('s_user_account.id'), nullable=False)
    goods_count = db.Column(db.Integer, default=1)
    goods_price = db.Column(db.DECIMAL(10, 2))

    @classmethod
    def add_order_detail_info(cls, order_id, goods_id,passport_id, goods_count, goods_price):
        info = cls(
            order_id=order_id,
            goods_id=goods_id,
            passport_id=passport_id,
            goods_count=goods_count,
            goods_price=goods_price
        )
        db.session.add(info)
        db.session.commit()

    @classmethod
    def get_goods(cls, order_id):
        info = cls.query.filter_by(order_id=order_id).all()
        return info

    # @classmethod
    # def get_order_info(cls, pindex, per_page, passport_id):
    #     print(db.session.query(OrderDetail).filter(Orders.passport_id).order_by(OrderDetail.create_time.desc()).all())
    #     pagination = db.session.query(OrderDetail).filter(Orders.passport_id).order_by(OrderDetail.create_time.desc()).\
    #         paginate(
    #         page=pindex,
    #         per_page=per_page,
    #         error_out=False
    #     )
    #     return pagination








