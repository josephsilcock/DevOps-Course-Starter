from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import List, Optional


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
    last_modification: datetime
    due: Optional[datetime] = None


class ItemView:
    def __init__(self, items: List[Item]):
        self.sorted_by_due_items = sorted(items, key=lambda item: (item.due is None, item.due))
        self.in_progress = [item for item in self.sorted_by_due_items if item.status == Status.IN_PROGRESS]
        self.not_started = [item for item in self.sorted_by_due_items if item.status == Status.NOT_STARTED]
        # TODO hook this up to frontend
        self.should_show_all_done_items = False

    @property
    def completed(self) -> List[Item]:
        ordered_by_completion = sorted(
            [item for item in self.sorted_by_due_items if item.status == Status.COMPLETED],
            key=lambda item: item.last_modification,
            reverse=True,
        )
        if self.should_show_all_done_items or len(ordered_by_completion) < 5:
            return ordered_by_completion
        return [item for item in ordered_by_completion if item.last_modification.date() == datetime.today().date()]
