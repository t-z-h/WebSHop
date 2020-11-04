import json
from datetime import datetime
from io import BytesIO
from threading import Thread

from flask import render_template, request, jsonify, redirect, url_for, current_app, session, make_response, app, Flask
from flask_mail import Message
from sqlalchemy import func
from flask_uploads import IMAGES, UploadSet, configure_uploads

from chengse_project import mail, db
from chengse_project.captcha import Captcha
from chengse_project.goods.models import Collect, Goods, Browsing
from chengse_project.orders.models import Orders, OrderDetail
from chengse_project.user import user_bp
from chengse_project.utils.comment import login_require
from chengse_project.utils.get_hash import get_hash
from .models import Passport, Address, Area, HeadImage


@user_bp.route("/register/", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("h_user/Registered.html")
    else:
        # print(1)
        username = request.form.get("username")
        password = request.form.get("password")
        email = request.form.get("email")
        Passport.add_one_passport(
            username=username,
            password=password,
            email=email
        )
        send_email(username, password, email)
        info = Passport.query.filter_by(username=username).first()
        HeadImage.add_first_image(info.id)
        return redirect(url_for("user_bp.login"))


def async_send_email(app, msg):
    with app.app_context():
        mail.send(message=msg)


# 多线程发送邮件
def send_email(username, password, email):
    message = "<h1>欢迎您成为橙色商城会员</h1>请您保管好您的注册信息<br/>" + "用户名：" + username + "<br/>密码：" + password + "<br/>祝您生活愉快!"
    msg = Message(
        "",
        sender=current_app.config["MAIL_USERNAME"],
        recipients=[email],
        html=message
    )
    from chengse_project import create_app
    thread = Thread(target=async_send_email, args=(create_app("product"), msg))
    thread.start()


@user_bp.route("/check_user_exist/")
def check_user_exist():
    username = request.args.get("username")
    # print(username)
    passport = Passport.get_one_passport(username=username)
    # print(passport)
    if passport:
        # 用户名已存在
        return jsonify(res=0)
    else:
        # 用户名可用
        return jsonify(res=1)


@user_bp.route("/verify_code/", methods=["POST", "GET"])
def verify_code():
    text, image = Captcha.gene_graph_captcha()
    session["verify_code"] = text
    out = BytesIO()
    image.save(out, 'png')
    out.seek(0)
    resp = make_response(out.read())
    resp.content_type = "image/png"
    return resp


@user_bp.route("/login/")
def login():
    username = request.cookies.get("username", "")
    return render_template("h_user/Login.html", username=username)


@user_bp.route("/check_login/", methods=["GET", "POST"])
def check_username():
    if "GET" == request.method:
        username = request.args.get("username")
        passport = Passport.get_one_passport(username=username)
        if passport:
            return jsonify(res="exist")
        else:
            return jsonify(res="inexistence")
    else:
        username = request.form.get("username")
        password = request.form.get("password")
        remember = request.form.get("remember")
        obj = Passport.get_one_passport(username=username, password=password)
        if password == "":
            return jsonify(res="error_pwd")
        if obj:
            next_url = session.get("pre_url_path", "/")
            jres = jsonify(res="true_pwd", next_url=next_url)
            if "true" == remember:
                jres.set_cookie("username", username, max_age=30 * 24 * 3600)
            session["is_login"] = True
            session["username"] = username
            session["passport_id"] = obj.id
            return jres
        else:
            return jsonify(res="error_pwd")


@user_bp.route("/retrieve/")
def retrieve():
    return render_template("h_user/retrieve.html")


@user_bp.route("/check_ret_user/")
def check_ret_user():
    username = request.args.get("username")
    passport = Passport.get_one_passport(username=username)
    if passport:
        username = request.args.get("username")
        email = passport.email
        message = render_template(
            "h_user/email.html"
        )
        """render_template(
            "chongzhi.html",
            username=username
        )"""
        msg = Message(
            '',
            sender=current_app.config["MAIL_USERNAME"],
            recipients=[email],
            html=message
        )
        mail.send(msg)
        session["username"] = username
        return jsonify(res="exist")
    else:
        return jsonify(res="inexistence")


@user_bp.route("/chongzhi_pwd/", methods=["GET", "POST"])
def chongzhi_pwd():
    if request.method == "GET":
        time = str(datetime.now())[:19]
        return render_template("h_user/chongzhi.html", time=time)
    else:
        # print(session)
        username = session.get("username")
        pwd = request.form.get("pwd")
        Passport.query.filter_by(username=username).update({"password": get_hash(pwd)})
        db.session.commit()
        return redirect(url_for("user_bp.login"))


@user_bp.route("/check_yzm/")
def check_yzm():
    yzm = request.args.get("yzm")
    if session["verify_code"].lower() != yzm.lower():
        print(session["verify_code"].lower(), yzm.lower())
        return jsonify(res="yzm_error")
    else:
        return jsonify(res="yzm_true")


@user_bp.route("/help/")
def help():
    return render_template("h_user/help.html")


@user_bp.route("/orders_center/")
@login_require
def order_center():
    time = str(datetime.now())[:19]
    passport_id = session.get("passport_id")
    orders = Orders.search_orders_all(passport_id)
    history = Browsing.query.filter_by(passport_id=passport_id).order_by(Browsing.create_time.desc()).all()[0:9]
    order_info = OrderDetail.query.filter_by(passport_id=passport_id).all()
    print(order_info)
    head_pic = HeadImage.query.filter_by(passport_id=passport_id).all()
    username = session.get("username")
    info = Passport.get_one_passport(username=username)

    context = dict(
        order_info=order_info,
        info=info,
        time=time,
        orders=orders,
        orders_len=len(orders),
        history=history,
        head_pic=head_pic
    )
    return render_template("h_user/User1.html", **context)


photos = UploadSet("photos", IMAGES)
@user_bp.route("/user_center/", methods=["POST", "GET"])
@login_require
def user_center():
    if request.method == 'POST' and 'pic' in request.files:
        # 将文件保存到本地
        passport_id = session.get("passport_id")
        filename = photos.save(request.files['pic'])
        # 返回文件路径
        file_url = photos.url(filename)
        basename = photos.get_basename(filename)
        path = photos.path(filename)
        head_pic = f"{path[23:]}"
        time = str(datetime.now())[:19]
        # print("/static/"+head_pic)
        # print(HeadImage.query.filter_by(passport_id=passport_id).first())
        HeadImage.query.filter_by(passport_id=passport_id).update({"user_image": "/static/"+head_pic})
        db.session.commit()
        # session["head_pic"] = head_pic
        username = session.get("username")
        passport_id = session.get("passport_id")
        info = Passport.get_one_passport(username=username)
        addr = Address.get_one_address(passport_id)
        head_pic = HeadImage.query.filter_by(passport_id=passport_id).all()
        return render_template("h_user/User_Personalinfo.html", info=info, addr=addr, time=time, head_pic=head_pic)
    else:
        time = str(datetime.now())[:19]
        username = session.get("username")
        passport_id = session.get("passport_id")
        info = Passport.get_one_passport(username=username)
        addr = Address.get_one_address(passport_id)
        head_pic = HeadImage.query.filter_by(passport_id=passport_id).all()
        return render_template("h_user/User_Personalinfo.html", info=info, addr=addr, time=time, head_pic=head_pic)


@user_bp.route("/modify_info/", methods=["POST"])
def modify_info():
    user = session.get("username")
    sex = request.form.get("sex")
    if sex == "0":
        sex = "保密"
    elif sex == "1":
        sex = "男"
    else:
        sex = "女"
    phone = request.form.get("phone")
    email = request.form.get("email")
    print(email, sex, user, phone)
    Passport.query.filter_by(username=user).update({"email": email, "gender": sex, "phone": phone})
    db.session.commit()
    return redirect(url_for("user_bp.user_center"))


@user_bp.route("/address/")
@login_require
def address():
    time = str(datetime.now())[:19]
    username = session.get("username")
    info = Passport.get_one_passport(username=username)
    passport_id = session.get("passport_id")
    addr = Address.query.filter_by(passport_id=passport_id).all()
    head_pic = HeadImage.query.filter_by(passport_id=passport_id).all()
    province = Area.get_province()
    return render_template("h_user/User_address.html", addr=addr, info=info, time=time, head_pic=head_pic, province=province)


@user_bp.route("/city/")
def city():
    province_id = request.args.get("province", "110100")
    info = Area.get_addr_info(province_id)
    # print(info)
    return jsonify({"shi": info})


@user_bp.route("/county/")
def county():
    city_id = request.args.get("city", "110101")
    # print(city_id)
    info = Area.get_addr_info(city=city_id)
    # print(info)
    return jsonify({"county": info})


@user_bp.route("/add_address/", methods=["POST"])
def add_address():
    passport_id = session.get("passport_id")
    sheng = request.form.get("sheng")
    shi = request.form.get('shi')
    xian = request.form.get("xian")
    xiangxi = request.form.get("xiangxi")
    # print(sheng, shi, xian, xiangxi)
    sheng = Area.query.filter_by(aid=sheng).first()
    shi = Area.query.filter_by(aid=shi).first()
    xian = Area.query.filter_by(aid=xian).first()
    # print(sheng, shi, xian, xiangxi)
    addr = sheng.atitle + shi.atitle + xian.atitle + xiangxi
    name = request.form.get("name")
    zip_code = request.form.get("zip_code")
    phone = request.form.get("phone")
    Address.add_one_address(
        passport_id=passport_id,
        recipient_name=name,
        recipient_addr=addr,
        recipient_phone=phone,
        zip_code=zip_code
    )
    # addr = Address.query.filter_by(recipient_addr=xiangxi).first
    return redirect(url_for("user_bp.address"))


@user_bp.route("/modify_addr/<int:addr_id>/", methods=["GET", "POST"])
@login_require
def modify_addr(addr_id):
    if "GET" == request.method:
        username = session.get("username")
        info = Passport.get_one_passport(username=username)
        addr = Address.query.filter_by(id=addr_id).first()
        # print(addr)
        passport_id = session.get("passport_id")
        head_pic = HeadImage.query.filter_by(passport_id=passport_id).all()
        return render_template("h_user/change_addr.html", info=info, addr=addr, head_pic=head_pic)
    else:
        addr = request.form.get("addr")
        name = request.form.get("name")
        zip_code = request.form.get("zip_code")
        phone = request.form.get("phone")
        # print(addr, name, zip_code, phone)
        Address.query.filter_by(id=addr_id).update(
            {"recipient_addr": addr, "recipient_name": name, "zip_code": zip_code, "recipient_phone": phone})
        db.session.commit()
        return redirect(url_for("user_bp.address"))


# photos = UploadSet("photos", IMAGES)
# @user_bp.route("/uploads_image/", methods=["POST", "GET"])
# def uploads_image():
#     if request.method == 'POST' and 'pic' in request.files:
#         # 将文件保存到本地
#         filename = photos.save(request.files['pic'])
#         # 返回文件路径
#         file_url = photos.url(filename)
#         basename = photos.get_basename(filename)
#         path = photos.path(filename)
#         head_pic = "http://127.0.0.1:5000"+f"{path[15:]}"


@user_bp.route("/user_collect/")
@login_require
def user_collect():
    time = str(datetime.now())[:19]
    passport_id = session.get("passport_id")
    # print(passport_id)
    goods_id = session.get("goods_id")
    username = session.get("username")
    collect = db.session.query(Goods, Collect).filter(Collect.passport_id == passport_id, Goods.id == Collect.goods_id).all()
    count = Collect.query.filter(Collect.passport_id == passport_id).count()
    # print(count)
    # print(collect)
    head_pic = HeadImage.query.filter_by(passport_id=passport_id).all()
    info = Passport.get_one_passport(username=username)
    return render_template("h_user/User_Collect.html", info=info, collect=collect, count=count, time=time, head_pic=head_pic)


@user_bp.route("/delete_addr/<int:addr_id>")
def delete_addr(addr_id):
    # passport_id = session.get("passport_id")
    info = Address.query.get(addr_id)
    db.session.delete(info)
    db.session.commit()
    return redirect(url_for("user_bp.address"))


@user_bp.route("/change_pwd/")
@login_require
def change_pwd():
    time = str(datetime.now())[:19]
    username = session.get("username")
    info = Passport.get_one_passport(username=username)
    passport_id = session.get("passport_id")
    head_pic = HeadImage.query.filter_by(passport_id=passport_id).all()
    return render_template("h_user/User_changePassword.html", info=info, time=time, head_pic=head_pic)


@user_bp.route("/delete_collect/<int:goods_id>")
def delete_collect(goods_id):
    info = Collect.query.filter_by(goods_id=goods_id).first()
    db.session.delete(info)
    db.session.commit()
    return redirect(url_for("user_bp.user_collect"))


@user_bp.route("/change_pwd_exist/", methods=["POST", "GET"])
def change_pwd_exist():
    pre_password = request.form.get("pre_password")
    new_password = request.form.get("new_password")
    if pre_password == "":
        return jsonify(res=0)
    # print(new_password, pre_password)
    username = session.get("username")
    password = Passport.get_one_passport(username=username, password=pre_password)
    # print(password)
    if password:
        Passport.query.filter(Passport.username == username).update({"password": get_hash(new_password)})
        db.session.commit()
        return jsonify(res="success")
    else:
        return jsonify(res=0)


@user_bp.route("/logout/")
def logout():
    session.clear()
    return redirect('/')
