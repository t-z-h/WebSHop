from flask import Blueprint

goods_bp = Blueprint("goods_bp", __name__)


from . import views
