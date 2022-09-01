import os
from enum import Enum, auto

from flask_login import UserMixin


class Role(Enum):
    READER = auto()
    WRITER = auto()
    ADMIN = auto()


class User(UserMixin):
    def __init__(self, id: str, name: str = ""):
        self.id = id
        self.name = name
