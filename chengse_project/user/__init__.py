
from flask import Blueprint, copy_current_request_context, current_app
from flask_mail import Message

from chengse_project import mail

user_bp = Blueprint("user_bp", __name__)

# @copy_current_request_context
# def send_email(username, password, email):
#     message = "<h1>欢迎您成为橙色商城会员</h1>请您保管好您的注册信息<br/>" + "用户名：" + username + "<br/>密码：" + password + "<br/>祝您生活愉快!"
#     msg = Message(
#         "",
#         sender=current_app.config["MAIL_USERNAME"],
#         recipients=[email],
#         html=message
#     )
#
#     mail.send(msg)

from . import views


