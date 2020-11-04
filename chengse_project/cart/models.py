from chengse_project import db
from chengse_project.base_model.base_model import BaseModel
from chengse_project.goods.models import Goods


class Cart(BaseModel):
    __tablename__ = "carts"
    passport_id = db.Column(db.Integer, db.ForeignKey("s_user_account.id"), nullable=False)
    goods_id = db.Column(db.Integer, db.ForeignKey("s_goods.id"), nullable=False)
    goods_count = db.Column(db.Integer, default=1)

    @classmethod
    def get_one_cart_info(cls, passport_id, goods_id):
        cart_info = cls.query.filter_by(passport_id=passport_id, goods_id=goods_id).first()
        print(cart_info)
        return cart_info

    @classmethod
    def add_one_cart_info(cls, passport_id, goods_id, goods_count):
        cart_info = cls.get_one_cart_info(passport_id=passport_id, goods_id=goods_id)
        # 判断库存

        if cart_info:
            total_count = cart_info.goods_count + goods_count
            if total_count <= cart_info.goods.goods_stock:
                cart_info.goods_count = total_count
                db.session.add(cart_info)
                db.session.commit()
                return True
            else:
                return False
        else:
            # total_count = cart_info.goods_count + goods_count
            goods = Goods.query.get(goods_id)
            if goods_count <= goods.goods_stock:
                cart_info = Cart(
                    passport_id=passport_id,
                    goods_id=goods_id,
                    goods_count=goods_count
                )
                db.session.add(cart_info)
                db.session.commit()
                return True
            else:
                return False
        # if cart_info:
        #     total_count = cart_info.goods_count+goods_count
        #     cart_info.goods_count = total_count
        #     db.session.add(cart_info)
        #     db.session.commit()
        #     return True
        # else:
        #     goods = Goods.query.get(goods_id)
        #     cart_info = Cart(
        #         passport_id=passport_id,
        #         goods_id=goods_id,
        #         goods_count=goods_count
        #     )
        #     db.session.add(cart_info)
        #     db.session.commit()
        #     return True

    @classmethod
    def update_one_cart_info(cls, passport_id, goods_id, goods_count):
        cart_info = cls.get_one_cart_info(
            passport_id=passport_id,
            goods_id=goods_id
        )
        if goods_count <= cart_info.goods.goods_stock:
            cart_info.goods_count = goods_count
            db.session.add(cart_info)
            db.session.commit()
            return True
        else:
            return False

    @classmethod
    def delete_cart_info(cls, passport_id, goods_id):
        try:
            cart_info = cls.get_one_cart_info(
                passport_id=passport_id,
                goods_id=goods_id
            )
            db.session.delete(cart_info)
            db.session.commit()
            return True
        except:
            return False

    @classmethod
    def get_cart_list_by_id_list(cls, cart_id_list):
        """获取id在cart_id_list中的购物车记录"""
        cart_list = Cart.query.filter(Cart.id.in_(cart_id_list)).all()
        return cart_list

