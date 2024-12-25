import pytest

from homeinventory.stringbox import StringBox
from homeinventory.stringbox import exportcsv, importcsv, searchboxes


def test_newbox_empty():
    box = StringBox("mybox")
    assert len(box) == 0


def test_newbox_threeitems():
    box = StringBox("mybox", items=["Item 1", "Item 2", "Item 3"])
    assert len(box) == 3


def test_newbox_name():
    box = StringBox("mybox")
    assert box.name == "mybox"


@pytest.fixture
def boxfruit():
    box = StringBox("Fruit")
    box.add("Apples")
    box.add("Blueberries")
    box.add("Hazelnuts")
    box.add("Strawberries")
    return box


@pytest.fixture
def boxnuts():
    box = StringBox("Nuts")
    box.add("Almonds")
    box.add("Cashews")
    box.add("Hazelnuts")
    box.add("Pecans")
    return box


def test_boxiter(boxfruit):
    lastfruit = ""
    for fruit in boxfruit:
        lastfruit = fruit
    assert lastfruit == "Strawberries"


def test_boxadd(boxfruit):
    oldlen = len(boxfruit)
    boxfruit.add("Kiwis")
    assert len(boxfruit) == oldlen+1


def test_boxadd_twoinstances(boxfruit, boxnuts):
    oldlen = len(boxfruit)
    boxnuts.add("Walnuts")
    assert len(boxfruit) == oldlen


def test_boxremove(boxfruit):
    oldlen = len(boxfruit)
    boxfruit.remove("Apples")
    assert len(boxfruit) == oldlen-1


def test_boxsearch_nomatch(boxfruit):
    matches = boxfruit.search("Pecans")
    assert len(matches) == 0


def test_boxsearch_allmatch(boxfruit):
    matches = boxfruit.search("")
    assert len(matches) == len(boxfruit)


def test_boxsearch_onematch(boxfruit):
    matches = boxfruit.search("Strawberries")
    assert len(matches) == 1


def test_boxsearch_twomatches(boxfruit):
    matches = boxfruit.search("berries")
    assert len(matches) == 2


def test_boxsearch_caseinsensitive(boxfruit):
    matches = boxfruit.search("BERRIES")
    assert len(matches) == 2


def test_save(tmp_path, boxfruit):
    csvpath = tmp_path / "boxfruit.csv"
    exportcsv(str(csvpath), [boxfruit])
    linecount = 0
    with csvpath.open() as f:
        for _ in f:
            linecount += 1
    assert linecount == 5


def test_load(tmp_path, boxfruit, boxnuts):
    csvpath = tmp_path / "boxes.csv"
    exportcsv(str(csvpath), [boxfruit, boxnuts])
    boxes = importcsv(str(csvpath))
    assert len(boxes) == 2
    assert len(boxes["Fruit"]) == 4


def test_search(boxfruit, boxnuts):
    matches = searchboxes([boxfruit, boxnuts], "Hazelnuts")
    assert len(matches) == 2
