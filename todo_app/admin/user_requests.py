import os
from typing import List

import pymongo

from todo_app.login.user import User, Role


class DbUser:
    def __init__(self, github_id: str, role: int, name: str):
        self.github_id = github_id
        self.role = role
        self.name = name


class UserView:
    def __init__(self, users: List[DbUser]):
        self.sorted_by_name_users = sorted(users, key=lambda user: user.name)

    @property
    def admin(self) -> List[DbUser]:
        return [user for user in self.sorted_by_name_users if user.role == Role.ADMIN.value]

    @property
    def writer(self) -> List[DbUser]:
        return [user for user in self.sorted_by_name_users if user.role == Role.WRITER.value]

    @property
    def reader(self) -> List[DbUser]:
        return [user for user in self.sorted_by_name_users if user.role == Role.READER.value]


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
                "role": role.value,
                "githubName": user.name,
            }
        )

    def user_is_authorised(self, user: User, role: Role) -> bool:
        db_user = self.collection.find_one({"githubId": int(user.id)})
        return db_user['role'] >= role.value

    def get_users(self) -> UserView:
        return UserView([DbUser(user['githubId'], user['role'], user['githubName']) for user in self.collection.find()])

    def change_role(self, github_id: str, new_role: Role) -> None:
        self.collection.update_one(
            {"githubId": int(github_id)}, {"$set": {"role": new_role.value}}
        )
