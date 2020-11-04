from flask import Blueprint

cart_bp = Blueprint("cart_bp", __name__)


from . import views
