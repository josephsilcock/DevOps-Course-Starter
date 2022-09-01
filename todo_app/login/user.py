import os
from enum import Enum, auto

from flask_login import UserMixin, current_user


class Role(Enum):
    READER = auto()
    WRITER = auto()
    ADMIN = auto()


class User(UserMixin):
    def __init__(self, id: str):
        self.id = id
