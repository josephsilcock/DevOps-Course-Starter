import os
from datetime import datetime
from typing import Dict, List

import mongomock
import pymongo
import pytest
from bson import ObjectId
from dotenv import find_dotenv, load_dotenv
from flask import request
from pymongo.collection import Collection

from todo_app import app
from todo_app.data.items import Item, Status


class StubResponse:
    def __init__(self, fake_response_data: List[Dict], ok=True):
        self.fake_response_data = fake_response_data
        self.ok = ok

    def json(self) -> List[Dict]:
        return self.fake_response_data


@pytest.fixture
def client():
    file_path = find_dotenv(".env.test")
    load_dotenv(file_path, override=True)

    with mongomock.patch(servers=(("fakemongo.com", 27017),)):
        test_app = app.create_app()

        with test_app.test_client() as client:
            yield client


@pytest.fixture
def collection() -> Collection:
    client = pymongo.MongoClient(os.getenv("MONGODB_CONNECTION_STRING"))
    db = client[os.getenv("DB_NAME")]
    return db["items"]


def set_db_items(collection: Collection, items: List[Item]):
    collection.insert_many(
        [
            {
                "_id": ObjectId(item.id_),
                "title": item.title,
                "status": item.status.value,
                "description": item.description,
                "due": item.due,
                "last_modified": item.last_modification,
            }
            for item in items
        ]
    )


def test_index_page_with_no_items(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "To Do" not in response.data.decode()
    assert "In Progress" not in response.data.decode()
    assert "Completed" not in response.data.decode()
    assert "Add item to do" in response.data.decode()


def test_index_page_with_to_do_items(client, collection):
    _COMPLETED_ITEM = Item(
        "62f646a4dc7d350ccd91b02a", "test name", "test description", Status.COMPLETED, datetime(2022, 1, 21), None
    )
    _IN_PROGRESS_ITEM = Item(
        "62f646a4dc7d350ccd91b02b", "test name", "test description", Status.IN_PROGRESS, datetime(2022, 1, 21), None
    )
    _NOT_STARTED_ITEM = Item(
        "62f646a4dc7d350ccd91b02c", "test name", "test description", Status.NOT_STARTED, datetime(2022, 1, 21), None
    )
    set_db_items(collection, [_COMPLETED_ITEM, _IN_PROGRESS_ITEM, _NOT_STARTED_ITEM])

    response = client.get("/")
    assert response.status_code == 200
    assert "To Do" in response.data.decode()
    assert "In Progress" in response.data.decode()
    assert "Complete Items" in response.data.decode()
    assert "Add item to do" in response.data.decode()


@pytest.mark.parametrize(
    "data",
    [
        pytest.param({"title": "testtitle", "description": "", "due-date": ""}, id="Just title"),
        pytest.param(
            {"title": "testtitle", "description": "test description", "due-date": "2022-01-23"}, id="Just title"
        ),
    ],
)
def test_add_items_makes_correct_post(client, data):
    response = client.post("/add-item", data=data, follow_redirects=True)
    assert response.status_code == 200
    assert request.path == "/"
    assert "To Do" in response.data.decode()
    assert "In Progress" not in response.data.decode()
    assert "Complete Items" not in response.data.decode()
    assert data["title"] in response.data.decode()


def test_remove_items_makes_correct_delete(client, collection):
    delete_id = "62f646a4dc7d350ccd91b02a"

    set_db_items(
        collection,
        [
            Item(delete_id, "to be deleted", "test description", Status.COMPLETED, datetime(2022, 1, 21), None),
            Item(
                "62f646a4dc7d350ccd91b02b",
                "to remain",
                "test description",
                Status.COMPLETED,
                datetime(2022, 1, 21),
                None,
            ),
        ],
    )

    response = client.post("/delete-item", data={"id": delete_id}, follow_redirects=True)

    assert response.status_code == 200
    assert request.path == "/"
    assert "To Do" not in response.data.decode()
    assert "In Progress" not in response.data.decode()
    assert "Complete Items" in response.data.decode()
    assert "to be deleted" not in response.data.decode()
    assert "to remain" in response.data.decode()


@pytest.mark.parametrize("endpoint", ["/complete-item", "/start-item"])
def test_update_items_makes_correct_update(client, collection, endpoint):
    test_id = "62f646a4dc7d350ccd91b02a"
    set_db_items(
        collection, [Item(test_id, "test name", "test description", Status.NOT_STARTED, datetime(2022, 1, 21), None)]
    )

    response = client.post(endpoint, data={"id": test_id}, follow_redirects=True)
    assert response.status_code == 200
    assert request.path == "/"
    assert "To Do" not in response.data.decode()
    assert ("In Progress" if endpoint == "/start-item" else "Complete Items") in response.data.decode()
    assert ("In Progress" if endpoint != "/start-item" else "Complete Items") not in response.data.decode()
    assert "test name" in response.data.decode()
