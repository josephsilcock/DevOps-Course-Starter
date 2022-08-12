import os
from datetime import datetime
from typing import Dict, Union

import pymongo
from bson import ObjectId

from todo_app.data.items import Item, ItemView, Status


class MongoDbRequests:
    def __init__(self):
        client = pymongo.MongoClient(os.getenv("MONGODB_CONNECTION_STRING"))
        db = client[os.getenv("DB_NAME")]
        self.collection = db["items"]

    def _json_to_item(self, json: Dict[str, Union[str, datetime]]) -> Item:
        return Item(
            id_=json["_id"],
            status=Status(json["status"]),
            title=json["title"],
            description=json["description"],
            last_modification=json["last_modified"],
            due=datetime.fromisoformat(json["due"]) if json["due"] else None,
        )

    def get_items(self) -> ItemView:
        return ItemView([self._json_to_item(item) for item in self.collection.find()])

    def add_item(self, title: str, description: str, due: str) -> None:
        self.collection.insert_one(
            {
                "title": title,
                "status": Status.NOT_STARTED.value,
                "description": description,
                "due": due,
                "last_modified": datetime.now(),
            }
        )

    def remove_item(self, id_: str) -> None:
        self.collection.delete_one({"_id": ObjectId(id_)})

    def update_item_status(self, id_: str, new_status: Status) -> None:
        self.collection.update_one(
            {"_id": ObjectId(id_)}, {"$set": {"status": new_status.value, "lastModified": datetime.now()}}
        )
