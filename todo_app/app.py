from flask import Flask, render_template, request, redirect

from todo_app.data.session_items import (
    get_items,
    add_item,
    remove_item,
    get_item,
    save_item,
    Status,
)
from todo_app.flask_config import Config

app = Flask(__name__)
app.config.from_object(Config())


@app.route("/")
def index():
    completed_items = []
    incomplete_items = []
    for item in sorted(get_items(), key=lambda item: item["id"]):
        if item["status"] == Status.COMPLETED:
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
    add_item(request.values.get("title"))
    return redirect("/")


@app.route("/delete-item", methods=["POST"])
def delete_item():
    remove_item(request.values.get("id"))
    return redirect("/")


@app.route("/complete-item", methods=["POST"])
def complete_item():
    item = get_item(request.values.get("id"))
    item["status"] = "Completed"
    save_item(item)
    return redirect("/")
