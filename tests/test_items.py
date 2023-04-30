from tests.fixtures import an_item_type_1, an_item_type_2, multiple_items


def test_search_for(multiple_items):
    item = multiple_items.items[0]
    found_item = multiple_items.search_for(item.name)
    assert [item] == found_item


def test_item_names(multiple_items):
    names = [item.name for item in multiple_items.items]
    found_names = multiple_items.item_names()
    assert names == found_names


def test_get_item_by_id(multiple_items):
    item = multiple_items.items[0]
    assert item == multiple_items.get_item_by_id(item.id)


def test_get_item_by_name(multiple_items):
    item = multiple_items.items[0]
    assert item == multiple_items.get_item_by_name(item.name)


def test_get_item_by_names(multiple_items):
    items = multiple_items.items
    assert items == multiple_items.get_item_by_names([item.name for item in items])
