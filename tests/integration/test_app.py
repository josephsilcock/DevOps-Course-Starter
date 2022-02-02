import contextlib
import os
from dataclasses import replace
from datetime import datetime
from typing import Dict, List
from unittest import mock

import pytest
from dotenv import find_dotenv, load_dotenv
from flask import request

from tests.helpers.requests import item_to_json, test_status
from todo_app import app
from todo_app.data.exceptions import ResponseError
from todo_app.data.items import Item, Status


class StubResponse:
    def __init__(self, fake_response_data: List[Dict], ok=True):
        self.fake_response_data = fake_response_data
        self.ok = ok

    def json(self) -> List[Dict]:
        return self.fake_response_data


@pytest.fixture
def patch_trello_start_requests():
    def _get(url, params):
        if url == f"https://api.trello.com/1/boards/{os.environ.get('TRELLO_BOARD_ID')}/lists":
            return StubResponse([{"id": id_, "name": status.value} for status, id_ in test_status.items()])
        return []

    with mock.patch(f"todo_app.data.trello_items.requests") as mock_requests:
        mock_requests.get.side_effect = _get
        yield


@pytest.fixture
def patch_trello_error_start_requests():
    with mock.patch(f"todo_app.data.trello_items.requests") as mock_requests:
        mock_requests.get.side_effect = lambda url, params: StubResponse([], False)
        yield


@pytest.fixture
def client():
    file_path = find_dotenv(".env.test")
    load_dotenv(file_path, override=True)

    test_app = app.create_app()

    with test_app.test_client() as client:
        yield client


@contextlib.contextmanager
def patch_get_items(items: List[Item]):
    def _get(url, params):
        if url == f"https://api.trello.com/1/boards/{os.environ.get('TRELLO_BOARD_ID')}/cards":
            return StubResponse([item_to_json(item) for item in items])
        return []

    with mock.patch(f"todo_app.data.trello_items.requests") as mock_requests:
        mock_requests.get.side_effect = _get
        yield mock_requests


@pytest.mark.xfail(raises=ResponseError)
def test_failing_trello_requests_startup_redirects_to_error(patch_trello_error_start_requests, client):
    client.get("/")


def test_index_page_with_no_items(patch_trello_start_requests, client):
    with patch_get_items([]):
        response = client.get("/")
        assert response.status_code == 200
        assert "To Do" not in response.data.decode()
        assert "In Progress" not in response.data.decode()
        assert "Completed" not in response.data.decode()
        assert "Add item to do" in response.data.decode()


def test_index_page_with_to_do_items(patch_trello_start_requests, client):
    _COMPLETED_ITEM = Item("test id", "test name", "test description", Status.COMPLETED, datetime(2022, 1, 21), None)
    _IN_PROGRESS_ITEM = replace(_COMPLETED_ITEM, status=Status.IN_PROGRESS)
    _NOT_STARTED_ITEM = replace(_COMPLETED_ITEM, status=Status.NOT_STARTED)
    with patch_get_items([_COMPLETED_ITEM, _IN_PROGRESS_ITEM, _NOT_STARTED_ITEM]):
        response = client.get("/")
        assert response.status_code == 200
        assert "To Do" in response.data.decode()
        assert "In Progress" in response.data.decode()
        assert "Complete Items" in response.data.decode()
        assert "Add item to do" in response.data.decode()


@pytest.mark.parametrize(
    "data,response_ok",
    [
        pytest.param({"title": "test"}, True, id="Just title"),
        pytest.param(
            {"title": "test", "description": "test description", "due-date": "2022-01-23"}, True, id="Just title"
        ),
        pytest.param({}, False, id="Bad request"),
    ],
)
def test_add_items_makes_correct_post(patch_trello_start_requests, client, data, response_ok):
    def _post(url, params):
        return StubResponse([], params["name"] is not None)

    with patch_get_items([]) as mock_requests:
        mock_requests.post.side_effect = _post

        response = client.post("/add-item", data=data, follow_redirects=True)
        assert response.status_code == 200
        assert request.path == ("/" if response_ok else "/add-item")
        if not response_ok:
            assert "Something went wrong" in response.data.decode()
        mock_requests.post.assert_called_with(
            "https://api.trello.com/1/cards",
            params={
                "key": os.getenv("TRELLO_KEY"),
                "token": os.getenv("TRELLO_TOKEN"),
                "name": data.get("title"),
                "idList": test_status[Status.NOT_STARTED],
                "desc": data.get("description"),
                "due": data.get("due-date"),
            },
        )


@pytest.mark.parametrize("response_ok", [True, False])
def test_remove_items_makes_correct_delete(patch_trello_start_requests, client, response_ok):
    def _delete(url, params):
        return StubResponse([], response_ok)

    with patch_get_items([]) as mock_requests:
        mock_requests.delete.side_effect = _delete

        response = client.post("/delete-item", data={"id": 1}, follow_redirects=True)
        assert response.status_code == 200
        assert request.path == ("/" if response_ok else "/delete-item")
        if not response_ok:
            assert "Something went wrong" in response.data.decode()
        mock_requests.delete.assert_called_with(
            "https://api.trello.com/1/cards/1",
            params={
                "key": os.getenv("TRELLO_KEY"),
                "token": os.getenv("TRELLO_TOKEN"),
            },
        )


@pytest.mark.parametrize("response_ok", [True, False])
@pytest.mark.parametrize("endpoint", ["/complete-item", "/start-item"])
def test_update_items_makes_correct_put(patch_trello_start_requests, client, response_ok, endpoint):
    def _put(url, params):
        return StubResponse([], response_ok)

    with patch_get_items([]) as mock_requests:
        mock_requests.put.side_effect = _put

        response = client.post(endpoint, data={"id": 1}, follow_redirects=True)
        assert response.status_code == 200
        assert request.path == ("/" if response_ok else endpoint)
        if not response_ok:
            assert "Something went wrong" in response.data.decode()
        mock_requests.put.assert_called_with(
            "https://api.trello.com/1/cards/1",
            params={
                "key": os.getenv("TRELLO_KEY"),
                "token": os.getenv("TRELLO_TOKEN"),
                "idList": test_status[Status.COMPLETED if endpoint == "/complete-item" else Status.IN_PROGRESS],
            },
        )
