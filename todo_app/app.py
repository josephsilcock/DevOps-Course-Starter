from flask import Flask, redirect, render_template, request

from todo_app.data.items import Status
from todo_app.data.mongodb_requests import MongoDbRequests
from todo_app.flask_config import Config


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(Config())

    mongodb_requests = MongoDbRequests()

    @app.route("/")
    def index():
        return render_template("index.html", items=mongodb_requests.get_items())

    @app.route("/add-item", methods=["POST"])
    def add_item_to_items():
        mongodb_requests.add_item(
            request.values.get("title"), request.values.get("description"), request.values.get("due-date")
        )
        return redirect("/")

    @app.route("/delete-item", methods=["POST"])
    def delete_item():
        mongodb_requests.remove_item(request.values.get("id"))
        return redirect("/")

    @app.route("/complete-item", methods=["POST"])
    def complete_item():
        mongodb_requests.update_item_status(request.values.get("id"), Status.COMPLETED)
        return redirect("/")

    @app.route("/start-item", methods=["POST"])
    def start_item():
        mongodb_requests.update_item_status(request.values.get("id"), Status.IN_PROGRESS)
        return redirect("/")

    return app
