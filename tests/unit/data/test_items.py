from datetime import date
from typing import List

import pytest

from todo_app.data.items import Item, ItemView, Status

_COMPLETED_ITEM = Item("test id", "test name", "test description", Status.COMPLETED, None)
_COMPLETED_ITEM_DUE_SOON = Item("test id", "test name", "test description", Status.COMPLETED, date(2022, 1, 21))
_COMPLETED_ITEM_DUE_NOT_SOON = Item("test id", "test name", "test description", Status.COMPLETED, date(2022, 3, 12))
_IN_PROGRESS_ITEM = Item("test id", "test name", "test description", Status.IN_PROGRESS, None)
_IN_PROGRESS_ITEM_DUE_SOON = Item("test id", "test name", "test description", Status.IN_PROGRESS, date(2022, 1, 21))
_IN_PROGRESS_ITEM_DUE_NOT_SOON = Item("test id", "test name", "test description", Status.IN_PROGRESS, date(2022, 3, 12))
_NOT_STARTED_ITEM = Item("test id", "test name", "test description", Status.NOT_STARTED, None)
_NOT_STARTED_ITEM_DUE_SOON = Item("test id", "test name", "test description", Status.NOT_STARTED, date(2022, 1, 21))
_NOT_STARTED_ITEM_DUE_NOT_SOON = Item("test id", "test name", "test description", Status.NOT_STARTED, date(2022, 3, 12))


@pytest.mark.parametrize(
    "items,completed_items",
    [
        pytest.param([_COMPLETED_ITEM], [_COMPLETED_ITEM], id="single completed item"),
        pytest.param(
            [_COMPLETED_ITEM, _IN_PROGRESS_ITEM, _NOT_STARTED_ITEM],
            [_COMPLETED_ITEM],
            id="completed item, and other different status items",
        ),
        pytest.param(
            [_COMPLETED_ITEM, _COMPLETED_ITEM_DUE_SOON, _COMPLETED_ITEM_DUE_NOT_SOON],
            [_COMPLETED_ITEM_DUE_SOON, _COMPLETED_ITEM_DUE_NOT_SOON, _COMPLETED_ITEM],
            id="orders completed items by date properly",
        ),
    ],
)
def test_item_view_completed_items(items: List[Item], completed_items: List[Item]):
    assert ItemView(items).completed == completed_items


@pytest.mark.parametrize(
    "items,in_progress_items",
    [
        pytest.param([_IN_PROGRESS_ITEM], [_IN_PROGRESS_ITEM], id="single in progress item"),
        pytest.param(
            [_COMPLETED_ITEM, _IN_PROGRESS_ITEM, _NOT_STARTED_ITEM],
            [_IN_PROGRESS_ITEM],
            id="in progress item, and other different status items",
        ),
        pytest.param(
            [_IN_PROGRESS_ITEM, _IN_PROGRESS_ITEM_DUE_SOON, _IN_PROGRESS_ITEM_DUE_NOT_SOON],
            [_IN_PROGRESS_ITEM_DUE_SOON, _IN_PROGRESS_ITEM_DUE_NOT_SOON, _IN_PROGRESS_ITEM],
            id="orders in progress items by date properly",
        ),
    ],
)
def test_item_view_in_progress_items(items: List[Item], in_progress_items: List[Item]):
    assert ItemView(items).in_progress == in_progress_items


@pytest.mark.parametrize(
    "items,not_started_items",
    [
        pytest.param([_NOT_STARTED_ITEM], [_NOT_STARTED_ITEM], id="single not started item"),
        pytest.param(
            [_COMPLETED_ITEM, _IN_PROGRESS_ITEM, _NOT_STARTED_ITEM],
            [_NOT_STARTED_ITEM],
            id="not started item, and other different status items",
        ),
        pytest.param(
            [_NOT_STARTED_ITEM, _NOT_STARTED_ITEM_DUE_SOON, _NOT_STARTED_ITEM_DUE_NOT_SOON],
            [_NOT_STARTED_ITEM_DUE_SOON, _NOT_STARTED_ITEM_DUE_NOT_SOON, _NOT_STARTED_ITEM],
            id="orders not started items by date properly",
        ),
    ],
)
def test_item_view_not_started_items(items: List[Item], not_started_items: List[Item]):
    assert ItemView(items).not_started == not_started_items
