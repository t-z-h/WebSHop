from threading import Thread

from flask import Flask, request, session, g
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
from flask_uploads import configure_uploads, UploadSet, IMAGES

# from chengse_project.user.views import photos
from config import config_map

db = SQLAlchemy()
mail = Mail()


def create_app(config_name):
    app = Flask(__name__)
    # 根据配置模型类的名字获取配置参数类
    config_class = config_map[config_name]
    app.config.from_object(config_class)
    db.init_app(app)

    # 注册蓝图
    from chengse_project import user, goods, cart, orders
    app.register_blueprint(user.user_bp, url_prefix="/user")
    app.register_blueprint(goods.goods_bp)
    app.register_blueprint(cart.cart_bp, url_prefix="/cart")
    app.register_blueprint(orders.order_bp, url_prefix="/order")

    # 使用app初始化mail
    mail.init_app(app)

    photos = UploadSet("photos", IMAGES)
    configure_uploads(app, photos)

    @app.before_request
    def url_path_record():
        """记录请求的url"""
        exclude_path = ["/user/login/", "/user/register/", "/user/logout/", "/user/verify_code/", "/user/retrieve/", "/user/chongzhi_pwd/", "/user/change_pwd/"]
        if request.path not in exclude_path and not request.is_xhr and "/static" not in request.path and "/Products" not in request.path and "/products" not in request.path and "/images" not in request.path and "/favicon.ico" not in request.path :
            session["pre_url_path"] = request.path
    return app






