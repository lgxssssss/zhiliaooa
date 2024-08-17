from flask import Blueprint, render_template, jsonify, redirect, url_for
from exts import mail, db
from flask_mail import Message
from flask import request
from models import EmailCaptchaModel
import string
import random
from .forms import RegisterForm
from models import UserModel
from werkzeug.security import generate_password_hash, check_password_hash

bp = Blueprint("auth", __name__, url_prefix='/auth')
@bp.route("/login")
def login():
    return "欢迎来到login"

# GET：从服务器上获取数据
# POST：将客户端的数据提交给服务器
@bp.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    else:
        # 验证用户提交的邮箱和验证码是否对应且正确
        # 表单验证：flask-wtf: wtforms
        form = RegisterForm(request.form)
        if form.validate():
            email = form.email.data
            username = form.username.data
            password = form.password.data
            user = UserModel(email=email, username=username, password=generate_password_hash(password))
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("auth.login"))
        else:
            print(form.errors)
            return redirect(url_for("auth.register"))

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