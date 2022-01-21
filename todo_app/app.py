from flask import Flask, redirect, render_template, request

from todo_app.data.exceptions import ResponseError
from todo_app.data.trello_items import Status, TrelloRequests
from todo_app.flask_config import Config


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(Config())

    trello_requests = TrelloRequests()

    try:
        trello_requests.init_lists()
    except ResponseError:
        redirect("/error")

    def _catch_request_errors(func):
        def wrap(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except ResponseError:
                return redirect("/error")

        return wrap

    @app.route("/", endpoint="index")
    @_catch_request_errors
    def index():
        return render_template("index.html", items=trello_requests.get_items())

    @app.route("/add-item", endpoint="add_item_to_items", methods=["POST"])
    @_catch_request_errors
    def add_item_to_items():
        trello_requests.add_item(
            request.values.get("title"), request.values.get("description"), request.values.get("due-date")
        )
        return redirect("/")

    @app.route("/delete-item", endpoint="delete_item", methods=["POST"])
    @_catch_request_errors
    def delete_item():
        trello_requests.remove_item(request.values.get("id"))
        return redirect("/")

    @app.route("/complete-item", endpoint="complete_item", methods=["POST"])
    @_catch_request_errors
    def complete_item():
        trello_requests.update_item_status(request.values.get("id"), Status.COMPLETED)
        return redirect("/")

    @app.route("/start-item", endpoint="start_item", methods=["POST"])
    @_catch_request_errors
    def start_item():
        trello_requests.update_item_status(request.values.get("id"), Status.IN_PROGRESS)
        return redirect("/")

    @app.route("/error")
    def error_page():
        return render_template("error.html")

    return app
