"""Manage the home inventory database."""
from pathlib import Path
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


class DatabaseNotConnectedError(Exception):
    pass


class InventoryDatabase:
    """Interface for the database."""
    def __init__(self) -> None:
        self.connection: sqlite3.Connection | None = None

    def add_inventoryitem(self, name: str, unitid: int,
                          description: str) -> int:
        """Add an inventory item."""
        if not self.connection:
            raise DatabaseNotConnectedError
        cursor = self.connection.execute(
            "INSERT INTO InventoryItem(name, unitid, description)"
            " VALUES (?, ?, ?)", (name, unitid, description))
        self.connection.commit()
        itemid = cursor.lastrowid
        if not itemid:
            raise RuntimeError("Unable to create new InventoryItem record")
        return itemid

    def create(self, filename: str) -> None:
        """Create the database if it does not exist."""
        path = Path(filename)
        if path.exists():
            raise RuntimeError(f"File or directory exists: " + filename)
        connection = sqlite3.connect(filename)
        cursor = connection.cursor()
        cursor.executescript(CREATEDB_SQL)
        units = [("each", "ea"), ("feet", "ft"), ("inches", "in"),
                 ("centimeters", "cm"), ("millimeters", "mm")]
        cursor.executemany("INSERT INTO InventoryItemUnit(name, symbol)"
                           " VALUES (?, ?)", units)
        connection.commit()
        self.connection = connection

    def fetchall_inventoryitem(self) -> list[InventoryItem]:
        """Get all inventory items from the database."""
        if not self.connection:
            raise DatabaseNotConnectedError
        cursor = self.connection.cursor()
        result = []
        for row in cursor.execute("SELECT * FROM InventoryItem"):
            result.append(InventoryItem(*row))
        return result

    def fetchall_inventoryitemunit(self) -> list[InventoryItemUnit]:
        """Get all inventory items from the database."""
        if not self.connection:
            raise DatabaseNotConnectedError
        cursor = self.connection.cursor()
        result = []
        for row in cursor.execute("SELECT * FROM InventoryItemUnit"):
            result.append(InventoryItemUnit(*row))
        return result

    def open(self, filename: str) -> None:
        """Open the database."""
        self.connection = sqlite3.connect(filename)
