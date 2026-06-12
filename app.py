import os
from datetime import datetime, UTC
from functools import wraps
from pathlib import Path

from flask import Flask, abort, flash, make_response, redirect, render_template, request, url_for
from flask_login import LoginManager, UserMixin, current_user, login_required, login_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DATABASE_PATH = DATA_DIR / "app.db"

db = SQLAlchemy()
login_manager = LoginManager()


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default="user")
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(UTC))
    last_login_at = db.Column(db.DateTime, nullable=True)

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-secret-key-change-me")
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DATABASE_PATH}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "login"
    login_manager.login_message = "请先登录后再继续。"

    def asset_url(filename: str) -> str:
        static_file = Path(app.static_folder) / filename
        version = int(static_file.stat().st_mtime) if static_file.exists() else 0
        return url_for("static", filename=filename, v=version)

    app.jinja_env.globals["asset_url"] = asset_url

    @app.context_processor
    def inject_now() -> dict[str, datetime]:
        return {"now": datetime.now(UTC)}

    register_routes(app)

    with app.app_context():
        init_database()

    return app


@login_manager.user_loader
def load_user(user_id: str) -> User | None:
    return db.session.get(User, int(user_id))


def admin_required(view):
    @wraps(view)
    @login_required
    def wrapped_view(*args, **kwargs):
        if current_user.role != "admin":
            abort(403)
        return view(*args, **kwargs)

    return wrapped_view


def init_database() -> None:
    DATA_DIR.mkdir(exist_ok=True)
    db.create_all()

    seed_users = [
        ("admin", "Admin@123456", "admin"),
        ("user1", "User@123456", "user"),
    ]

    for username, password, role in seed_users:
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            continue

        user = User(username=username, role=role)
        user.set_password(password)
        db.session.add(user)

    db.session.commit()


def validate_username(username: str) -> str | None:
    if len(username) < 3:
        return "用户名至少需要 3 个字符。"
    if len(username) > 32:
        return "用户名不能超过 32 个字符。"
    if not username.replace("_", "").replace("-", "").isalnum():
        return "用户名只允许字母、数字、下划线和短横线。"
    return None


def validate_password(password: str) -> str | None:
    if len(password) < 8:
        return "密码至少需要 8 个字符。"
    return None


def register_routes(app: Flask) -> None:
    @app.route("/")
    def home():
        if not current_user.is_authenticated:
            return redirect(url_for("login"))
        return redirect(url_for("quote"))

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for("quote"))

        if request.method == "POST":
            username = request.form.get("username", "").strip()
            password = request.form.get("password", "")
            user = User.query.filter_by(username=username).first()

            if not user or not user.check_password(password):
                flash("用户名或密码错误。", "error")
                return render_template("login.html"), 401

            if not user.is_active:
                flash("当前账户已被停用，请联系管理员。", "error")
                return render_template("login.html"), 403

            user.last_login_at = datetime.now(UTC)
            db.session.commit()
            login_user(user)
            flash("登录成功。", "success")
            next_url = request.args.get("next")
            return redirect(next_url or url_for("quote"))

        return render_template("login.html")

    @app.route("/logout", methods=["POST"])
    @login_required
    def logout():
        logout_user()
        flash("已退出登录。", "success")
        return redirect(url_for("login"))

    @app.route("/quote")
    @login_required
    def quote():
        response = make_response(render_template("index.html"))
        response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
        return response

    @app.route("/records")
    @login_required
    def records():
        return redirect(url_for("quote"))

    @app.route("/account")
    @login_required
    def account():
        return render_template("account.html")

    @app.route("/account/password", methods=["POST"])
    @login_required
    def account_change_password():
        current_password = request.form.get("current_password", "")
        new_password = request.form.get("new_password", "")
        confirm_password = request.form.get("confirm_password", "")

        if not current_user.check_password(current_password):
            flash("当前密码不正确。", "error")
            return redirect(url_for("account"))

        password_error = validate_password(new_password)
        if password_error:
            flash(password_error, "error")
            return redirect(url_for("account"))

        if new_password != confirm_password:
            flash("两次输入的新密码不一致。", "error")
            return redirect(url_for("account"))

        current_user.set_password(new_password)
        db.session.commit()
        flash("密码已更新。", "success")
        return redirect(url_for("account"))

    @app.route("/admin")
    @admin_required
    def admin_dashboard():
        stats = {
            "total_users": User.query.count(),
            "admin_users": User.query.filter_by(role="admin").count(),
            "normal_users": User.query.filter_by(role="user").count(),
            "active_users": User.query.filter_by(is_active=True).count(),
        }
        recent_users = User.query.order_by(User.created_at.desc()).limit(5).all()
        return render_template("admin_dashboard.html", stats=stats, recent_users=recent_users)

    @app.route("/admin/users")
    @admin_required
    def admin_users():
        users = User.query.order_by(User.role.asc(), User.created_at.asc()).all()
        return render_template("admin_users.html", users=users)

    @app.route("/admin/users/create", methods=["POST"])
    @admin_required
    def admin_users_create():
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        role = request.form.get("role", "user").strip()

        username_error = validate_username(username)
        if username_error:
            flash(username_error, "error")
            return redirect(url_for("admin_users"))

        password_error = validate_password(password)
        if password_error:
            flash(password_error, "error")
            return redirect(url_for("admin_users"))

        if role not in {"admin", "user"}:
            flash("角色参数不合法。", "error")
            return redirect(url_for("admin_users"))

        if User.query.filter_by(username=username).first():
            flash("用户名已存在，请更换。", "error")
            return redirect(url_for("admin_users"))

        user = User(username=username, role=role)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash(f"账户 {username} 已创建。", "success")
        return redirect(url_for("admin_users"))

    @app.route("/admin/users/<int:user_id>/toggle-active", methods=["POST"])
    @admin_required
    def admin_users_toggle_active(user_id: int):
        user = db.session.get(User, user_id)
        if user is None:
            abort(404)

        if user.id == current_user.id:
            flash("不能停用当前登录的管理员账户。", "error")
            return redirect(url_for("admin_users"))

        user.is_active = not user.is_active
        db.session.commit()
        status_text = "启用" if user.is_active else "停用"
        flash(f"账户 {user.username} 已{status_text}。", "success")
        return redirect(url_for("admin_users"))

    @app.route("/admin/users/<int:user_id>/reset-password", methods=["POST"])
    @admin_required
    def admin_users_reset_password(user_id: int):
        user = db.session.get(User, user_id)
        if user is None:
            abort(404)

        new_password = request.form.get("new_password", "")
        password_error = validate_password(new_password)
        if password_error:
            flash(f"{user.username} 重置失败：{password_error}", "error")
            return redirect(url_for("admin_users"))

        user.set_password(new_password)
        db.session.commit()
        flash(f"账户 {user.username} 密码已重置。", "success")
        return redirect(url_for("admin_users"))

    @app.route("/admin/users/<int:user_id>/rename", methods=["POST"])
    @admin_required
    def admin_users_rename(user_id: int):
        user = db.session.get(User, user_id)
        if user is None:
            abort(404)

        new_username = request.form.get("username", "").strip()
        username_error = validate_username(new_username)
        if username_error:
            flash(f"{user.username} 修改失败：{username_error}", "error")
            return redirect(url_for("admin_users"))

        existing_user = User.query.filter_by(username=new_username).first()
        if existing_user and existing_user.id != user.id:
            flash("新用户名已存在，请更换。", "error")
            return redirect(url_for("admin_users"))

        old_username = user.username
        user.username = new_username
        db.session.commit()
        flash(f"账户 {old_username} 已改名为 {new_username}。", "success")
        return redirect(url_for("admin_users"))

    @app.route("/admin/users/<int:user_id>/change-role", methods=["POST"])
    @admin_required
    def admin_users_change_role(user_id: int):
        user = db.session.get(User, user_id)
        if user is None:
            abort(404)

        new_role = request.form.get("role", "").strip()
        if new_role not in {"admin", "user"}:
            flash("角色参数不合法。", "error")
            return redirect(url_for("admin_users"))

        if user.id == current_user.id and new_role != "admin":
            flash("不能把当前登录的管理员账户降级为普通用户。", "error")
            return redirect(url_for("admin_users"))

        old_role = user.role
        user.role = new_role
        db.session.commit()
        flash(f"账户 {user.username} 角色已从 {old_role} 改为 {new_role}。", "success")
        return redirect(url_for("admin_users"))

    @app.route("/admin/users/<int:user_id>/delete", methods=["POST"])
    @admin_required
    def admin_users_delete(user_id: int):
        user = db.session.get(User, user_id)
        if user is None:
            abort(404)

        if user.id == current_user.id:
            flash("不能删除当前登录的管理员账户。", "error")
            return redirect(url_for("admin_users"))

        if user.role == "admin":
            admin_count = User.query.filter_by(role="admin").count()
            if admin_count <= 1:
                flash("不能删除系统中的最后一个管理员账户。", "error")
                return redirect(url_for("admin_users"))

        username = user.username
        db.session.delete(user)
        db.session.commit()
        flash(f"账户 {username} 已删除。", "success")
        return redirect(url_for("admin_users"))

    @app.errorhandler(403)
    def forbidden(_error):
        return render_template("403.html"), 403


app = create_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
