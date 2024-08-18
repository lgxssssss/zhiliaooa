from flask import Blueprint, request, render_template

bp = Blueprint("qa", __name__, url_prefix='/')
@bp.route("/")
def login():
    return "欢迎来到首页"

@bp.route("/qa/public", methods=['GET', 'POST'])
def qa():
    if request .method == 'GET':
        return render_template("public_question.html")