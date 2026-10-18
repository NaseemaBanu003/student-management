from flask import Blueprint, render_template

web_bp = Blueprint("web", __name__)


@web_bp.route("/")
def index():
    return render_template("index.html")


@web_bp.route("/login")
def login_page():
    return render_template("index.html")


@web_bp.route("/dashboard")
def dashboard_page():
    return render_template("index.html")
