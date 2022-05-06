from dataclasses import replace
from datetime import datetime
from typing import List
from unittest import mock

import pytest

from todo_app.data.items import Item, ItemView, Status

_TODAY = datetime(2022, 1, 18)

_COMPLETED_ITEM = Item("test id", "test name", "test description", Status.COMPLETED, datetime(2022, 1, 21), None)
_COMPLETED_ITEM_FINISHED_EARLIER = replace(
    _COMPLETED_ITEM, last_modification=datetime(2022, 1, 18), due=datetime(2022, 1, 25)
)

_IN_PROGRESS_ITEM = replace(_COMPLETED_ITEM, status=Status.IN_PROGRESS)
_IN_PROGRESS_ITEM_DUE_SOON = replace(_IN_PROGRESS_ITEM, due=datetime(2022, 1, 21))
_IN_PROGRESS_ITEM_DUE_NOT_SOON = replace(_IN_PROGRESS_ITEM, due=datetime(2022, 3, 12))

_NOT_STARTED_ITEM = replace(_COMPLETED_ITEM, status=Status.NOT_STARTED)
_NOT_STARTED_ITEM_DUE_SOON = replace(_NOT_STARTED_ITEM, due=datetime(2022, 1, 21))
_NOT_STARTED_ITEM_DUE_NOT_SOON = replace(_NOT_STARTED_ITEM, due=datetime(2022, 3, 12))


@pytest.fixture
def patch_today():
    with mock.patch(f"{ItemView.__module__}.datetime") as mock_datetime:
        mock_datetime.today.return_value = _TODAY
        yield


@pytest.mark.parametrize(
    "items,completed_items",
    [
        pytest.param([_COMPLETED_ITEM], [_COMPLETED_ITEM], id="single completed item"),
        pytest.param(
            [_COMPLETED_ITEM, _IN_PROGRESS_ITEM, _NOT_STARTED_ITEM],
            [],
            id="completed item, and other different status items",
        ),
        pytest.param(
            [_COMPLETED_ITEM_FINISHED_EARLIER, _COMPLETED_ITEM],
            [],
            id="orders completed items by completed date properly",
        ),
    ],
)
def test_item_view_completed_items(items: List[Item], completed_items: List[Item]):
    assert ItemView(items).completed == completed_items


def test_should_show_all_done_items(patch_today):
    today_items = [replace(_COMPLETED_ITEM, last_modification=_TODAY) for _ in range(5)]
    other_items = [replace(_COMPLETED_ITEM, last_modification=datetime(2022, 1, 10)) for _ in range(5)]
    item_view = ItemView(today_items + other_items)

    assert item_view.completed == today_items

    item_view.should_show_all_done_items = True

    assert item_view.completed == today_items + other_items


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
            id="orders in progress items by due date properly",
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
            id="orders not started items by due date properly",
        ),
    ],
)
def test_item_view_not_started_items(items: List[Item], not_started_items: List[Item]):
    assert ItemView(items).not_started == not_started_items
