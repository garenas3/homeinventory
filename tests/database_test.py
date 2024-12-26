import pytest 
import sqlite3

import homeinventory.database as database
from homeinventory import InventoryItem, InventoryItemUnit


@pytest.fixture
def connection():
    result_connection = sqlite3.connect(":memory:")
    database.initialize(result_connection)
    return result_connection


def test_initialize(connection):
    cursor = connection.cursor()
    resultset = cursor.execute("SELECT unitid"
                               " FROM InventoryItemUnit"
                               " WHERE name = 'each'")
    unitid, = resultset.fetchone()
    assert unitid == 1
    resultset = cursor.execute("SELECT MAX(transactionid)"
                               " FROM InventoryTransaction"
                               " GROUP BY transactionid")
    transactionid, = resultset.fetchone()
    assert transactionid == 1


def test_fetchall_inventoryitemunit(connection):
    units = database.fetchall_inventoryitemunit(connection)
    assert len(units) > 1
    assert InventoryItemUnit(1, "each", "ea") in units


def test_create_inventoryitem(connection):
    name = "Test Item"
    unitid = 1
    notes = "This is a test item."
    itemid = database.create_inventoryitem(connection, name, unitid, notes)
    cursor = connection.cursor()
    resultset = cursor.execute("SELECT name, unitid, notes"
                               " FROM InventoryItem"
                               " WHERE itemid = ?", (itemid,))
    assert (name, unitid, notes) == resultset.fetchone()


def test_fetchall_inventoryitem(connection):
    units = {unit.unitid: unit
             for unit in database.fetchall_inventoryitemunit(connection)}
    items = []
    for i in range(1, 4):
        name = f"Test Item {i}"
        unitid = i
        notes = f"This is test item {i}."
        itemid = database.create_inventoryitem(connection, name, unitid, notes)
        items.append(InventoryItem(itemid, name, units[unitid], notes))
    assert set(items) == set(database.fetchall_inventoryitem(connection,
                                                             units))


def test_update_inventoryitem(connection):
    name = "Test Item"
    unitid = 1
    notes = "This is a test item."
    itemid = database.create_inventoryitem(connection, name, unitid, notes)
    name = "Test Item (Updated)"
    unitid = 2
    notes = "This is a test item. (Updated)"
    database.update_inventoryitem(connection, itemid, name, unitid, notes)
    cursor = connection.cursor()
    resultset = cursor.execute("SELECT itemid, name, unitid, notes"
                               " FROM InventoryItem"
                               " WHERE itemid = ?", (itemid,))
    assert (itemid, name, unitid, notes) == resultset.fetchone()


def test_delete_inventoryitem(connection):
    name = "Test Item"
    unitid = 1
    notes = "This is a test item."
    itemid = database.create_inventoryitem(connection, name, unitid, notes)
    database.delete_inventoryitem(connection, itemid)
    cursor = connection.cursor()
    resultset = cursor.execute("SELECT 1"
                               " FROM InventoryItem"
                               " WHERE itemid = ?", (itemid,))
    assert not resultset.fetchone()


def test_current_inventorytransaction(connection):
    transactionid = database.current_inventorytransaction(connection)
    assert transactionid == 1
