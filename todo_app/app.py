from flask import Flask, render_template, request, redirect

from todo_app.data.session_items import get_items, add_item
from todo_app.flask_config import Config

app = Flask(__name__)
app.config.from_object(Config())


@app.route('/')
def index():
    return render_template("index.html", items=get_items())


@app.route("/add-item", methods=["POST"])
def add_item_to_items():
    add_item(request.values.get("title"))
    return redirect('/')
