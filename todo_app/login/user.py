import os
from enum import Enum, auto
from flask_login import UserMixin


class Role(Enum):
    READER = auto()
    WRITER = auto()


class User(UserMixin):
    def __init__(self, id: str):
        self.id = id

    @property
    def role(self) -> Role:
        if self.id == os.getenv("GITHUB_ID_WRITER"):
            return Role.WRITER
        return Role.READER
