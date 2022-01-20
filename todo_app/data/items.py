from dataclasses import dataclass
from datetime import date
from enum import Enum
from typing import Optional, List


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
    due: Optional[date]


class ItemView:
    def __init__(self, items: List[Item]):
        sorted_items = sorted(items, key=lambda item: (item.due is None, item.due))
        self.completed = [item for item in sorted_items if item.status == Status.COMPLETED]
        self.in_progress = [item for item in sorted_items if item.status == Status.IN_PROGRESS]
        self.not_started = [item for item in sorted_items if item.status == Status.NOT_STARTED]
