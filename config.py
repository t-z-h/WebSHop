import os
from local_setting import EMAIL_ADDR, EMAIL_PASSWORD


class Config(object):
    """配置基本参数"""
    SECRET_KEY = os.urandom(24)
    SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://root:root@127.0.0.1:3306/flask_project"
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SESSION_USE_SIGNER = 2 * 7 * 24 * 3600
    MAIL_SERVER = "smtp.163.com"
    MAIL_PROT = 465
    MAIL_USERNAME = EMAIL_ADDR         # 邮箱地址
    MAIL_PASSWORD = EMAIL_PASSWORD     # 邮箱配置的密码
    UPLOADED_PHOTOS_DEST = "chengse_project/static/uploads"
    ENABLE_THREADS = True


class DevelopmentConfig(Config):
    DEBUG = True


class ProductConfig(Config):
    pass


config_map = {
    "develop": DevelopmentConfig,
    "product": ProductConfig
}
