from flask import Flask, redirect, render_template, request
from flask_login import LoginManager, login_required, login_user

from todo_app.authentication.github import GithubAuthenticator
from todo_app.data.items import Status
from todo_app.data.mongodb_requests import MongoDbRequests
from todo_app.flask_config import Config
from todo_app.authentication.user import User


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(Config())

    mongodb_requests = MongoDbRequests()

    login_manager = LoginManager()

    authenticator = GithubAuthenticator()

    @app.route("/")
    @login_required
    def index():
        return render_template("index.html", items=mongodb_requests.get_items())

    @app.route("/add-item", methods=["POST"])
    @login_required
    def add_item_to_items():
        mongodb_requests.add_item(
            request.values.get("title"), request.values.get("description"), request.values.get("due-date")
        )
        return redirect("/")

    @app.route("/delete-item", methods=["POST"])
    @login_required
    def delete_item():
        mongodb_requests.remove_item(request.values.get("id"))
        return redirect("/")

    @app.route("/complete-item", methods=["POST"])
    @login_required
    def complete_item():
        mongodb_requests.update_item_status(request.values.get("id"), Status.COMPLETED)
        return redirect("/")

    @app.route("/start-item", methods=["POST"])
    @login_required
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

    @login_manager.unauthorized_handler
    def unauthenticated():
        return redirect(authenticator.login_url)

    @login_manager.user_loader
    def load_user(user_id) -> User:
        return User(user_id)

    login_manager.init_app(app)

    return app


