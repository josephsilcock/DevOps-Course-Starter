from todo_app.data.items import Item

test_status = {
    "Not Started": 1,
    "In Progress": 2,
    "Completed": 3,
}


def item_to_json(item: Item):
    return {
        "id": item.id_,
        "idList": test_status[item.status.value],
        "name": item.title,
        "desc": item.description,
        "dateLastActivity": item.last_modification.isoformat(),
        "due": item.due.isoformat() if item.due is not None else None,
    }
