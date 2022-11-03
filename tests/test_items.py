from tests.fixtures import an_item_type_1, an_item_type_2, multiple_items, item_set_without_nones, item_set_with_nones


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


def test_item_set_repaired_names(item_set_without_nones):
    names = item_set_without_nones.repaired_names
    assert names == ["weapon", "helm", "body", "shield", "legs"]


def test_item_set_repaired_names_with_nones(item_set_with_nones):
    names = item_set_with_nones.repaired_names
    assert names == ["weapon", "helm", "body", "legs"]


def test_item_set_broken_names(item_set_without_nones):
    names = item_set_without_nones.broken_pieces_name
    assert names == ["weapon 0", "helm 0", "body 0", "shield 0", "legs 0"]


def test_item_set_broken_names_with_nones(item_set_with_nones):
    names = item_set_with_nones.broken_pieces_name
    assert names == ["weapon 0", "helm 0", "body 0", "legs 0"]


def test_item_set_find_key(item_set_without_nones):
    name = item_set_without_nones.weapon
    assert name == item_set_without_nones.find_key(name)

