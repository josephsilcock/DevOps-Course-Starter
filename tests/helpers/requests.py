from todo_app.data.items import Item, Status

test_status = {
    Status.NOT_STARTED: 1,
    Status.IN_PROGRESS: 2,
    Status.COMPLETED: 3,
}


def item_to_json(item: Item):
    return {
        "id": item.id_,
        "idList": test_status[item.status],
        "name": item.title,
        "desc": item.description,
        "dateLastActivity": item.last_modification.isoformat(),
        "due": item.due.isoformat() if item.due is not None else None,
    }
