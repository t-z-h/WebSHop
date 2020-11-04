from chengse_project import db
from chengse_project.base_model.base_model import BaseModel
from chengse_project.utils.get_hash import get_hash


class Passport(BaseModel):
    """用户模型类"""
    __tablename__ = "s_user_account"
    username = db.Column(db.String(20))
    password = db.Column(db.String(40))
    email = db.Column(db.String(30))
    gender = db.Column(db.String(3), default="保密")  # 默认为保密，1为男，2为女
    phone = db.Column(db.String(20), default=None)  # 默认为空
    balance = db.Column(db.Integer, default=2000)       # 用户余额
    integral = db.Column(db.Integer, default=1000)    # 积分

    @classmethod
    def add_one_passport(cls, username, password, email):
        obj = cls(
            username=username,
            password=get_hash(password),
            email=email
        )
        db.session.add(obj)
        db.session.commit()
        return obj

    @classmethod
    def get_one_passport(cls, username, password=None):
        """根据用户名查询信息"""
        query_dict = dict(
            username=username
        )
        if password:
            query_dict.update(password=get_hash(password))
        obj = cls.query.filter_by(**query_dict).first()
        return obj


class Address(BaseModel):
    """地址模型类"""
    __tablename__ = "s_user_address"
    recipient_name = db.Column(db.String(24))
    recipient_addr = db.Column(db.String(256))
    recipient_phone = db.Column(db.String(11))
    zip_code = db.Column(db.String(6))  # 邮编地址
    is_default = db.Column(db.Boolean, default=False)  # 是否为默认地址
    passport_id = db.Column(db.Integer, db.ForeignKey("s_user_account.id"), nullable=False)

    @classmethod
    def add_one_address(cls, passport_id, recipient_name, recipient_addr, recipient_phone, zip_code):
        """添加应该收货地址"""
        addr = cls.get_one_address(passport_id=passport_id)
        obj = cls(
            passport_id=passport_id,
            recipient_name=recipient_name,
            recipient_addr=recipient_addr,
            recipient_phone=recipient_phone,
            zip_code=zip_code,
            is_default=not bool(addr)
        )
        db.session.add(obj)
        db.session.commit()
        return obj

    @classmethod
    def get_one_address(cls, passport_id):
        addr = Address.query.filter_by(passport_id=passport_id).first()
        print(addr)
        return addr


# class Orders(BaseModel):
#     __tablename__ = "orders"
#     passport_id = db.Column(db.Integer, db.ForeignKey("s_user_account.id"), nullable=False)
#     order_num = db.Column(db.String(20))
#     goods_count = db.Column(db.Integer)
#     goods_id = db.Column(db.Integer, db.ForeignKey("s_goods.id"), nullable=False)


class Area(db.Model):
    __tablename__ = "areas"
    aid = db.Column(db.Integer, primary_key=True)    # 邮编
    atitle = db.Column(db.String(20))    # 地名
    pid = db.Column(db.Integer)

    @classmethod
    def get_province(cls):
        province = cls.query.filter_by(pid=None).all()
        print(province)
        return province

    @classmethod
    def get_addr_info(cls, province_id=None, city=None):
        if province_id:
            res = []
            info = db.session.query(Area).filter(Area.pid == province_id).all()
            for shi in info:
                res.append([str(shi.aid), str(shi.atitle)])
            return res
        if city:
            res = []
            info = db.session.query(Area).filter(Area.pid == city).all()
            for shi in info:
                res.append([str(shi.aid), str(shi.atitle)])
            return res


class HeadImage(BaseModel):
    __tablename__ = "head_image"
    passport_id = db.Column(db.Integer, db.ForeignKey("s_user_account.id"), nullable=False)
    user_image = db.Column(db.String(60), default="/static/images/people.png")

    @classmethod
    def add_first_image(cls, passport_id):
        info = cls(passport_id=passport_id,
                   user_image="/static/images/people.png")
        db.session.add(info)
        db.session.commit()
