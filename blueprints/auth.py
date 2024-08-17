from flask import Blueprint, render_template, jsonify
from exts import mail, db
from flask_mail import Message
from flask import request
from models import EmailCaptchaModel
import string
import random

bp = Blueprint("auth", __name__, url_prefix='/auth')
@bp.route("/login")
def login():
    pass

@bp.route("/register")
def register():
    return render_template("register.html")

@bp.route("/captcha/email")
def get_email_captcha():
    email = request.args.get("email")
    source = string.digits * 4
    captcha = random.sample(source, 4)
    captcha = "".join(captcha)
    message = Message(subject="知了传课注册验证码", recipients=[email], body=f"您的验证码是：{captcha}")
    mail.send(message)
    email_captcha = EmailCaptchaModel(email=email, captcha=captcha)
    db.session.add(email_captcha)
    db.session.commit()
    # RESTful API
    # {code: 200/400/500, message: "", data: {}}
    return jsonify({"code": 200, "message": "", "data": None})

@bp.route("/mail/test")
def mial_test():
    message = Message(subject="邮箱测试", recipients=["2713508347@qq.com"], body="这是一条测试邮件")
    mail.send(message)
    return "邮件发送成功！"