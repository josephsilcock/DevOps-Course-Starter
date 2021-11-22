from dataclasses import dataclass
from enum import Enum


class Status(str, Enum):
    NOT_STARTED = "Not Started"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"


@dataclass
class Item:
    id_: str
    title: str
    description: str
    status: Status
