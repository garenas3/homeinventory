"""Manage the home inventory database."""
import sqlite3

from .common import InventoryItem, InventoryItemUnit


class RecordNotUpdatedError(Exception):
    pass


class RecordNotDeletedError(Exception):
    pass


class NoCurrentInventoryTransactionError(Exception):
    pass


CREATEDB_SQL = """
CREATE TABLE InventoryItemUnit(
    unitid INTEGER PRIMARY KEY ASC,
    name   TEXT UNIQUE,
    symbol TEXT
);
CREATE TABLE InventoryItem(
    itemid INTEGER PRIMARY KEY ASC,
    name   TEXT,
    unitid INTEGER,
    notes  TEXT,
    FOREIGN KEY(unitid) REFERENCES InventoryItemUnit(unitid)
);
CREATE TABLE InventoryTransaction(
    transactionid INTEGER PRIMARY KEY ASC
);
"""


def initialize(connection: sqlite3.Connection) -> None:
    """Initialize the database.

    Create tables and initialize data for a new database. Do not call
    this function more than once for the life of the database.

    Some state is guaranteed on creation. The "each" unit will always
    have a `unitid` of 1. No other `unitid` value is guaranteed. Common
    lengths are added for convenience. The first inventory transaction
    with a `transactionid` of 1 will be initiated. The current
    `transactionid` will always be the largest `transactionid`.
    """
    cursor = connection.cursor()
    cursor.executescript(CREATEDB_SQL)
    units = [("each", "ea"), ("feet", "ft"), ("inches", "in"), ("meters", "m"),
             ("centimeters", "cm"), ("millimeters", "mm")]
    cursor.executemany("INSERT INTO InventoryItemUnit(name, symbol)"
                       " VALUES (?, ?)", units)
    cursor.execute("INSERT INTO InventoryTransaction DEFAULT VALUES")
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
    return [InventoryItem(itemid, name, units[unitid], notes)
            for itemid, name, unitid, notes in resultset]


def create_inventoryitem(connection: sqlite3.Connection, name: str,
                         unitid: int, notes: str) -> int:
    """Add an inventory item.

    Args:
        connection: The connection to the SQLite database.
        name: A short description of the item.
        unitid: The unit ID of the unit of measure. This should match a
            record in the InventoryItemUnit table.
        notes: Additional information about the item.

    Returns:
        The `itemid` of the item created in the database.
    """
    cursor = connection.execute(
        "INSERT INTO InventoryItem(name, unitid, notes)"
        " VALUES (?, ?, ?)", (name, unitid, notes))
    connection.commit()
    itemid = cursor.lastrowid
    if not itemid:
        raise RuntimeError("Unable to create new InventoryItem record")
    return itemid


def update_inventoryitem(connection: sqlite3.Connection, itemid: int,
                         name: str, unitid: int, notes: str) -> None:
    """Update an inventory item with the matching itemid."""
    cursor = connection.cursor()
    cursor.execute(
        "UPDATE InventoryItem"
        " SET name = ?, unitid = ?, notes = ?"
        " WHERE itemid = ?",
        (name, unitid, notes, itemid))
    connection.commit()
    if not cursor.rowcount:
        raise RecordNotUpdatedError()


def delete_inventoryitem(connection: sqlite3.Connection, itemid: int
                         ) -> None:
    """Delete an inventory item with the matching itemid."""
    cursor = connection.cursor()
    cursor.execute("DELETE FROM InventoryItem WHERE itemid = ?", (itemid,))
    connection.commit()
    if not cursor.rowcount:
        raise RecordNotDeletedError()


def create_inventorytransaction(connection: sqlite3.Connection) -> int:
    """Create a new inventory transaction.

    Args:
        connection: A connection to a SQLite database.

    Returns:
        The `transactionid` of the new transaction.
    """
    cursor = connection.execute(
            "INSERT INTO InventoryTransaction DEFAULT VALUES")
    connection.commit()
    transactid = cursor.lastrowid
    if not transactid:
        raise RuntimeError("Unable to create new InventoryTransaction record")
    return transactid


def current_inventorytransaction(connection: sqlite3.Connection) -> int:
    """Get the current transactid."""
    cursor = connection.cursor()
    cursor.execute("SELECT transactionid"
                   " FROM InventoryTransaction"
                   " ORDER BY transactionid DESC"
                   " LIMIT 1")
    row = cursor.fetchone()
    if not row:
        raise NoCurrentInventoryTransactionError
    return row[0]
