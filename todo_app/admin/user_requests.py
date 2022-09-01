import os

import pymongo

from todo_app.login.user import User, Role


class MongoDbUserRequests:
    def __init__(self):
        client = pymongo.MongoClient(os.getenv("MONGODB_CONNECTION_STRING"))
        db = client[os.getenv("DB_NAME")]
        self.collection = db["users"]

    def add_user(self, user: User) -> None:
        if self.collection.find_one({"githubId": int(user.id)}) is not None:
            return
        role = Role.ADMIN if len(list(self.collection.find())) == 0 else Role.READER
        self.collection.insert_one(
            {
                "githubId": user.id,
                "role": role.value
            }
        )

    def user_is_authorised(self, user: User, role: Role) -> bool:
        db_user = self.collection.find_one({"githubId": int(user.id)})
        return db_user['role'] > role.value
