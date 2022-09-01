import os
from random import randint
from typing import Optional

import requests
from flask import request

from todo_app.login.user import User


class GithubAuthenticator:
    def __init__(self):
        self.state = str(randint(10000000000000, 99999999999999))
        self.access_token = None
        self.user_id = None
        self.user_name = None

    @property
    def login_url(self) -> str:
        client_id = os.getenv("GITHUB_CLIENT_ID")
        return f"https://github.com/login/oauth/authorize?client_id={client_id}&state={self.state}"

    def is_genuine_response(self) -> bool:
        return request.values.get("state") == self.state

    def get_token(self) -> None:
        token_request = requests.post(
            "https://github.com/login/oauth/access_token",
            params={
                "client_id": os.getenv("GITHUB_CLIENT_ID"),
                "client_secret": os.getenv("GITHUB_CLIENT_SECRET"),
                "code": request.values.get("code"),
            },
            headers={"Accept": "application/json"},
        )
        self.access_token = token_request.json()["access_token"]

    def get_user_details(self) -> None:
        if not self.is_genuine_response():
            return
        self.get_token()
        id_post = requests.get("https://api.github.com/user", headers={"Authorization": f"Bearer {self.access_token}"})
        self.user_id = id_post.json()["id"]
        self.user_name = id_post.json()["login"]

    def get_user(self) -> Optional[User]:
        if not self.is_genuine_response():
            return
        self.get_token()
        self.get_user_details()
        return User(self.user_id, self.user_name)
