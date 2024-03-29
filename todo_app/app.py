from functools import wraps
from logging import Formatter

from flask import Flask, redirect, render_template, request
from flask_login import LoginManager, current_user, login_required, login_user
from loggly.handlers import HTTPSHandler

from todo_app.admin.user_requests import MongoDbUserRequests
from todo_app.data.items import Status
from todo_app.data.mongodb_requests import MongoDbRequests
from todo_app.flask_config import Config
from todo_app.login.github import GithubAuthenticator
from todo_app.login.user import Role, User


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(Config())

    app.logger.setLevel(app.config["LOG_LEVEL"])
    if app.config["LOGGLY_TOKEN"] is not None:
        handler = HTTPSHandler(f'https://logs-01.loggly.com/inputs/{app.config["LOGGLY_TOKEN"]}/tag/todo-app')
        handler.setFormatter(Formatter("[%(asctime)s] %(levelname)s in %(module)s: %(message)s"))
        app.logger.addHandler(handler)

    item_requests = MongoDbRequests()
    user_requests = MongoDbUserRequests()

    login_manager = LoginManager()

    authenticator = GithubAuthenticator()

    def _is_authorised(role: Role):
        def _is_authorised_for_role(func):
            @wraps(func)
            def wrap(*args, **kwargs):
                if user_requests.user_is_authorised(current_user, role):
                    return func(*args, **kwargs)
                app.logger.warning(f"User: {current_user.id} attempted to access a site requiring role {role.name}")
                return redirect("/unauthorized")

            return wrap

        return _is_authorised_for_role

    @app.route("/")
    @login_required
    def index():
        return render_template(
            "index.html", items=item_requests.get_items(), role=user_requests.get_user_role(current_user)
        )

    @app.route("/add-item", methods=["POST"])
    @login_required
    @_is_authorised(Role.WRITER)
    def add_item_to_items():
        item_requests.add_item(
            request.values.get("title"), request.values.get("description"), request.values.get("due-date")
        )
        return redirect("/")

    @app.route("/delete-item", methods=["POST"])
    @login_required
    @_is_authorised(Role.WRITER)
    def delete_item():
        item_requests.remove_item(request.values.get("id"))
        return redirect("/")

    @app.route("/complete-item", methods=["POST"])
    @login_required
    @_is_authorised(Role.WRITER)
    def complete_item():
        item_requests.update_item_status(request.values.get("id"), Status.COMPLETED)
        return redirect("/")

    @app.route("/start-item", methods=["POST"])
    @login_required
    @_is_authorised(Role.WRITER)
    def start_item():
        item_requests.update_item_status(request.values.get("id"), Status.IN_PROGRESS)
        return redirect("/")

    @app.route("/admin")
    @login_required
    @_is_authorised(Role.ADMIN)
    def admin():
        return render_template("admin.html", users=user_requests.get_users())

    @app.route("/make-admin", methods=["POST"])
    @login_required
    @_is_authorised(Role.ADMIN)
    def make_admin():
        user_requests.change_role(request.values.get("id"), Role.ADMIN)
        return redirect("/admin")

    @app.route("/make-writer", methods=["POST"])
    @login_required
    @_is_authorised(Role.ADMIN)
    def make_writer():
        user_requests.change_role(request.values.get("id"), Role.WRITER)
        return redirect("/admin")

    @app.route("/make-reader", methods=["POST"])
    @login_required
    @_is_authorised(Role.ADMIN)
    def make_reader():
        user_requests.change_role(request.values.get("id"), Role.READER)
        return redirect("/admin")

    @app.route("/login/callback")
    def github_callback():
        user = authenticator.get_user()
        if user:
            user_requests.add_user(user)
            login_user(user)
            return redirect("/")
        return redirect("/unauthorized")

    @app.route("/unauthorized")
    def unauthorized():
        return render_template("unauthorized.html")

    @login_manager.unauthorized_handler
    def unauthenticated():
        return redirect(authenticator.login_url)

    @login_manager.user_loader
    def load_user(user_id: str) -> User:
        return User(user_id)

    login_manager.init_app(app)

    return app
