import os
from datetime import datetime
from typing import Dict, List, Optional

import requests

from todo_app.data.items import Item, Status


class TrelloRequests:
    def __init__(self):
        self.errored = False
        self._board_id: str = os.getenv("TRELLO_BOARD_ID")
        self._params: Dict[str, str] = {"key": os.getenv("TRELLO_KEY"), "token": os.getenv("TRELLO_TOKEN")}
        self._url = f"https://api.trello.com/1"
        self._lists_ids_to_names = None
        self._names_to_list_ids = None

    def init_list_maps(self) -> None:
        if self._lists_ids_to_names is None:
            self._lists_ids_to_names = self._get_lists()
            if self.errored:
                return
            self._names_to_list_ids = {v: k for k, v in self._lists_ids_to_names.items()}

    def _get_lists(self) -> Dict[str, Status]:
        r = self._get(f"{self._url}/boards/{self._board_id}/lists", self._params)
        return {l["id"]: Status(l["name"]) for l in r.json()} if r is not None else None

    def _json_to_item(self, json: Dict[str, str]) -> Item:
        return Item(
            id_=json["id"],
            status=self._lists_ids_to_names[json["idList"]],
            title=json["name"],
            description=json["desc"],
            due=datetime.strptime(json["due"][:10], "%Y-%m-%d") if json["due"] else None,
        )

    def _get(self, url: str, params: Dict[str, str]) -> requests.Response:
        r = requests.get(url, params=params)
        self._set_errored(r)
        return r if not self.errored else None

    def _set_errored(self, r: requests.Response) -> None:
        if not r.ok:
            self.errored = True

    def get_items(self) -> Optional[List[Item]]:
        r = self._get(f"{self._url}/boards/{self._board_id}/cards", self._params)
        return [self._json_to_item(item) for item in r.json()] if r is not None else None

    def add_item(self, title: str, description: str, due: str) -> None:
        post_params = self._params.copy()
        post_params.update(
            {
                "name": title,
                "idList": self._names_to_list_ids[Status.NOT_STARTED],
                "desc": description,
                "due": due,
            }
        )
        r = requests.post(f"{self._url}/cards", params=post_params)
        self._set_errored(r)

    def remove_item(self, id_: str) -> None:
        r = requests.delete(f"{self._url}/cards/{id_}", params=self._params)
        self._set_errored(r)

    def update_item_status(self, id_: str, new_status: Status) -> None:
        put_params = self._params.copy()
        put_params["idList"] = self._names_to_list_ids[new_status]
        r = requests.put(f"{self._url}/cards/{id_}", params=put_params)
        self._set_errored(r)
