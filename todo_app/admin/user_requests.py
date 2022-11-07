import os
from typing import List

import pymongo
from flask import current_app as app

from todo_app.login.user import Role, User


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

        app.logger.info(f"Adding user with id {user.id} and role {role.name}")

        self.collection.insert_one(
            {
                "githubId": int(user.id),
                "role": role.value,
                "githubName": user.name,
            }
        )

    def get_user_role(self, user: User) -> int:
        if login_is_disabled():
            return Role.ADMIN.value

        app.logger.info(f"Getting user role for user: {user.id}")

        db_user = self.collection.find_one({"githubId": int(user.id)})
        role = db_user["role"]

        app.logger.debug(f"Role found: {role}")

        return role

    def user_is_authorised(self, user: User, role: Role) -> bool:
        if login_is_disabled():
            return True
        app.logger.debug(f"Checking authorisation of user {user.id} for role {role.name}")

        is_authorised = self.get_user_role(user) >= role.value

        app.logger.debug(f"User is authorised: {is_authorised}")

        return is_authorised

    def get_users(self) -> UserView:
        app.logger.debug("Fetching users")

        return UserView([DbUser(user["githubId"], user["role"], user["githubName"]) for user in self.collection.find()])

    def change_role(self, github_id: str, new_role: Role) -> None:
        app.logger.info(f"Updating user role for user: {github_id}. New role: {new_role.name}")

        self.collection.update_one({"githubId": int(github_id)}, {"$set": {"role": new_role.value}})


def login_is_disabled() -> bool:
    if os.getenv("LOGIN_DISABLED") == "True":
        app.logger.critical("Login disabled - this should never happen!!")
        return True
    return False
