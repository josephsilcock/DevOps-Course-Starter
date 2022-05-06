import os
from datetime import datetime
from typing import Dict

import requests

from todo_app.data.items import Item, ItemView, Status
from todo_app.data.utils import catch_response_failure


class TrelloRequests:
    def __init__(self):
        self._board_id: str = os.getenv("TRELLO_BOARD_ID")
        self._params: Dict[str, str] = {"key": os.getenv("TRELLO_KEY"), "token": os.getenv("TRELLO_TOKEN")}
        self._url = "https://api.trello.com/1"
        self._lists_ids_to_names = None
        self._names_to_list_ids = None

    def init_lists(self):
        self._lists_ids_to_names = self._get_lists()
        self._names_to_list_ids = {v: k for k, v in self._lists_ids_to_names.items()}

    def _get_lists(self) -> Dict[str, Status]:
        r = self._get(f"{self._url}/boards/{self._board_id}/lists", self._params)
        return {list["id"]: Status(list["name"]) for list in r.json()}

    def _json_to_item(self, json: Dict[str, str]) -> Item:
        return Item(
            id_=json["id"],
            status=self._lists_ids_to_names[json["idList"]],
            title=json["name"],
            description=json["desc"],
            last_modification=datetime.fromisoformat(json["dateLastActivity"][:19]),
            due=datetime.fromisoformat(json["due"][:19]) if json["due"] else None,
        )

    @catch_response_failure
    def _get(self, url: str, params: Dict[str, str]) -> requests.Response:
        return requests.get(url, params=params)

    def get_items(self) -> ItemView:
        r = self._get(f"{self._url}/boards/{self._board_id}/cards", self._params)
        return ItemView([self._json_to_item(item) for item in r.json()])

    @catch_response_failure
    def add_item(self, title: str, description: str, due: str) -> requests.Response:
        post_params = self._params.copy()
        post_params.update(
            {
                "name": title,
                "idList": self._names_to_list_ids[Status.NOT_STARTED],
                "desc": description,
                "due": due,
            }
        )
        return requests.post(f"{self._url}/cards", params=post_params)

    @catch_response_failure
    def remove_item(self, id_: str) -> requests.Response:
        return requests.delete(f"{self._url}/cards/{id_}", params=self._params)

    @catch_response_failure
    def update_item_status(self, id_: str, new_status: Status) -> requests.Response:
        put_params = self._params.copy()
        put_params["idList"] = self._names_to_list_ids[new_status]
        return requests.put(f"{self._url}/cards/{id_}", params=put_params)
