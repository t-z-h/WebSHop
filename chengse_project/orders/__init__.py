from flask import Blueprint


order_bp = Blueprint("order_bp", __name__)

from . import views
