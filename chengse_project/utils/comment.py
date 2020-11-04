from functools import wraps

from flask import session, redirect, url_for


def login_require(view_func):
    """登陆判断装饰器"""
    @wraps(view_func)
    def wrapper(*view_args, **view_kwargs):
        print(session)
        if "is_login" in session:
            return view_func(*view_args, **view_kwargs)
        else:
            return redirect(url_for("user_bp.login"))

    return wrapper
