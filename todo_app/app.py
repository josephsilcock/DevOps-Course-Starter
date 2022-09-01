from functools import wraps

from flask import Flask, redirect, render_template, request
from flask_login import LoginManager, login_required, login_user, current_user

from todo_app.login.github import GithubAuthenticator
from todo_app.data.items import Status
from todo_app.data.mongodb_requests import MongoDbRequests
from todo_app.flask_config import Config
from todo_app.login.user import User, Role


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(Config())

    mongodb_requests = MongoDbRequests()

    login_manager = LoginManager()

    authenticator = GithubAuthenticator()

    def _writer_role_required(func):
        @wraps(func)
        def wrap(*args, **kwargs):
            if current_user.role == Role.READER:
                return func(*args, **kwargs)
            return redirect("/unauthorized")

        return wrap

    @app.route("/")
    @login_required
    def index():
        return render_template("index.html", items=mongodb_requests.get_items())

    @app.route("/add-item", methods=["POST"])
    @login_required
    @_writer_role_required
    def add_item_to_items():
        mongodb_requests.add_item(
            request.values.get("title"), request.values.get("description"), request.values.get("due-date")
        )
        return redirect("/")

    @app.route("/delete-item", methods=["POST"])
    @login_required
    @_writer_role_required
    def delete_item():
        mongodb_requests.remove_item(request.values.get("id"))
        return redirect("/")

    @app.route("/complete-item", methods=["POST"])
    @login_required
    @_writer_role_required
    def complete_item():
        mongodb_requests.update_item_status(request.values.get("id"), Status.COMPLETED)
        return redirect("/")

    @app.route("/start-item", methods=["POST"])
    @login_required
    @_writer_role_required
    def start_item():
        mongodb_requests.update_item_status(request.values.get("id"), Status.IN_PROGRESS)
        return redirect("/")

    @app.route("/login/callback")
    def github_callback():
        authenticator.get_user_id()
        if authenticator.user_id:
            user = User(authenticator.user_id)
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


