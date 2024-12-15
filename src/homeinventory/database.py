"""Manage the home inventory database."""
import sqlite3

from .common import InventoryItem, InventoryItemUnit


CREATEDB_SQL = """
CREATE TABLE InventoryItemUnit(
    unitid INTEGER PRIMARY KEY ASC,
    name   TEXT UNIQUE,
    symbol TEXT
);
CREATE TABLE InventoryItem(
    itemid      INTEGER PRIMARY KEY ASC,
    name        TEXT,
    unitid      INTEGER,
    description TEXT,
    FOREIGN KEY(unitid) REFERENCES InventoryItemUnit(unitid)
);
"""


def initialize(connection: sqlite3.Connection):
    """Initialize the database.

    Create the tables and initial data for a new database. Do not call
    this function more than once for the life of the database.
    """
    cursor = connection.cursor()
    cursor.executescript(CREATEDB_SQL)
    units = [("each", "ea"), ("feet", "ft"), ("inches", "in"), ("meters", "m"),
             ("centimeters", "cm"), ("millimeters", "mm")]
    cursor.executemany("INSERT INTO InventoryItemUnit(name, symbol)"
                       " VALUES (?, ?)", units)
    connection.commit()


def fetchall_inventoryitemunit(connection: sqlite3.Connection
                               ) -> list[InventoryItemUnit]:
    """Fetch all the units of measure."""
    cursor = connection.cursor()
    resultset = cursor.execute("SELECT * FROM InventoryItemUnit")
    return [InventoryItemUnit(*row) for row in resultset]


def fetchall_inventoryitem(connection: sqlite3.Connection,
                           units: dict[int, InventoryItemUnit]
                           ) -> list[InventoryItem]:
    """Fetch all inventory items.

    Args:
        connection: The connection to the SQLite database.
        units: A dictionary of units of measure whose keys are the
            `unitid` and whose values are the units. These units are
            used to build the inventory items.

    Returns:
        A list of inventory items.
    """
    cursor = connection.cursor()
    resultset = cursor.execute("SELECT * FROM InventoryItem")
    return [InventoryItem(itemid, name, units[unitid], description)
            for itemid, name, unitid, description in resultset]


def add_inventoryitem(connection: sqlite3.Connection, name: str, unitid: int,
                      description: str) -> int:
    """Add an inventory item.

    Args:
        connection: The connection to the SQLite database.
        name: A short description of the item.
        unitid: The unit ID of the unit of measure. This should match a
            record in the InventoryItemUnit table.
        description: Additional information about the item.

    Returns:
        The `itemid` of the item created in the database.
    """
    cursor = connection.execute(
        "INSERT INTO InventoryItem(name, unitid, description)"
        " VALUES (?, ?, ?)", (name, unitid, description))
    connection.commit()
    itemid = cursor.lastrowid
    if not itemid:
        raise RuntimeError("Unable to create new InventoryItem record")
    return itemid
