import os
from typing import Dict, List

import requests

from todo_app.data.items import Item, Status


class TrelloRequests:
    def __init__(self):
        self._board_id: str = os.getenv("TRELLO_BOARD_ID")
        self._params: Dict[str, str] = {
            "key": os.getenv("TRELLO_KEY"),
            "token": os.getenv("TRELLO_TOKEN")
        }
        self._url = f"https://api.trello.com/1"
        self._lists_ids_to_names = self._get_lists()
        self._names_to_list_ids = {v: k for k, v in self._lists_ids_to_names.items()}

    def _get_lists(self) -> Dict[str, Status]:
        return {
            l["id"]: Status(l["name"]) for l in requests.get(f"{self._url}/boards/{self._board_id}/lists", params=self._params).json()
        }

    def _json_to_item(self, json: Dict[str, str]) -> Item:
        return Item(id_=json["id"], status=self._lists_ids_to_names[json["idList"]], title=json["name"])

    def get_items(self) -> List[Item]:
        return [
            self._json_to_item(item) for item in requests.get(f"{self._url}/boards/{self._board_id}/cards", params=self._params).json()
        ]

    def get_item(self, id_: str) -> Item:
        return self._json_to_item(requests.get(f"{self._url}/boards/{self._board_id}/cards/{id_}", params=self._params).json())

    def add_item(self, title: str) -> Item:
        post_params = self._params.copy()
        post_params.update({"name": title, "idList": self._names_to_list_ids[Status.NOT_STARTED]})
        return self._json_to_item(requests.post(f"{self._url}/cards", params=post_params).json())

    def remove_item(self, id_: str) -> None:
        requests.delete(f"{self._url}/cards/{id_}", params=self._params)

    def update_item_status(self, id_: str, new_status: Status) -> Item:
        put_params = self._params.copy()
        put_params["idList"] = self._names_to_list_ids[new_status]
        return self._json_to_item(requests.put(f"{self._url}/cards/{id_}", params=put_params).json())
