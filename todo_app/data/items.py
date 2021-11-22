from dataclasses import dataclass
from datetime import date
from enum import Enum
from typing import Optional


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
