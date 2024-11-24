import pytest 

from homeinventory.database import InventoryDatabase
from homeinventory import InventoryItem, InventoryItemUnit


def test_create_inmemorydb():
    db = InventoryDatabase()
    db.create(":memory:")
    assert db.connection is not None
    cursor = db.connection.cursor()
    result = cursor.execute("SELECT name FROM sqlite_master")
    assert result.fetchone() is not None


@pytest.fixture
def invdb(tmp_path):
    dbpath = tmp_path / "inventory.db"
    db = InventoryDatabase()
    db.create(str(dbpath))
    return db


def test_create_filedb(invdb):
    assert invdb.connection is not None
    cursor = invdb.connection.cursor()
    result = cursor.execute("SELECT name FROM sqlite_master")
    assert result.fetchone() is not None


def test_fetchall_inventoryitemunit(invdb):
    units = invdb.fetchall_inventoryitemunit()
    assert isinstance(units[0], InventoryItemUnit)
    assert len(units) != 0


def test_fetchall_inventoryitem_someitems(invdb):
    items = invdb.fetchall_inventoryitem()
    assert len(items) == 0


def test_add_inventoryitem_oneitem(invdb):
    itemid = invdb.add_inventoryitem("Test Item", 1, "A short description.")
    assert itemid == 1
