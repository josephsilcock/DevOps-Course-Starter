from flask import Flask, redirect, render_template, request

from todo_app.data.trello_items import Status, TrelloRequests
from todo_app.flask_config import Config

app = Flask(__name__)
app.config.from_object(Config())


trello_requests = TrelloRequests()


@app.route("/")
def index():
    completed_items = []
    incomplete_items = []
    for item in sorted(trello_requests.get_items(), key=lambda item: item.id_):
        if item.status == Status.COMPLETED:
            completed_items.append(item)
        else:
            incomplete_items.append(item)

    return render_template(
        "index.html",
        completed_items=completed_items,
        incomplete_items=incomplete_items,
    )


@app.route("/add-item", methods=["POST"])
def add_item_to_items():
    trello_requests.add_item(request.values.get("title"))
    return redirect("/")


@app.route("/delete-item", methods=["POST"])
def delete_item():
    trello_requests.remove_item(request.values.get("id"))
    return redirect("/")


@app.route("/complete-item", methods=["POST"])
def complete_item():
    trello_requests.update_item_status(request.values.get("id"), Status.COMPLETED)
    return redirect("/")
