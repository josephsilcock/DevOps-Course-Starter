import json

from flask import Flask, redirect, render_template, request

from todo_app.data.exceptions import ResponseError
from todo_app.data.trello_items import Status, TrelloRequests
from todo_app.flask_config import Config


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(Config())

    trello_requests = TrelloRequests()

    trello_requests.init_lists()

    @app.route("/")
    def index():
        return render_template("index.html", items=trello_requests.get_items())

    @app.route("/add-item", methods=["POST"])
    def add_item_to_items():
        trello_requests.add_item(
            request.values.get("title"), request.values.get("description"), request.values.get("due-date")
        )
        return redirect("/")

    @app.route("/delete-item", methods=["POST"])
    def delete_item():
        trello_requests.remove_item(request.values.get("id"))
        return redirect("/")

    @app.route("/complete-item", methods=["POST"])
    def complete_item():
        trello_requests.update_item_status(request.values.get("id"), Status.COMPLETED)
        return redirect("/")

    @app.route("/start-item", methods=["POST"])
    def start_item():
        trello_requests.update_item_status(request.values.get("id"), Status.IN_PROGRESS)
        return redirect("/")

    @app.errorhandler(ResponseError)
    def error_page(e: ResponseError):
        return render_template("error.html", json=json.dumps(e.json, indent=2))

    return app
