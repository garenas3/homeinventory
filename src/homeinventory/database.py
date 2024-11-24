"""Manage the home inventory database."""
from pathlib import Path
import sqlite3

from .common import InventoryItem, InventoryItemUnit


class InventoryDatabase:
    """Interface for the database."""
    def __init__(self) -> None:
        self.connection: sqlite3.Connection | None = None

    def create(self, filename: str) -> None:
        """Create the database if it does not exist."""
        path = Path(filename)
        if path.exists():
            raise RuntimeError(f"File or directory exists: " + filename)
        connection = sqlite3.connect(filename)
        cursor = connection.cursor()

        cursor.execute("CREATE TABLE InventoryItemUnit("
                       "unitid INTEGER PRIMARY KEY ASC, name, symbol)")
        units = [("each", "ea"), ("feet", "ft"), ("inches", "in"),
                 ("centimeters", "cm"), ("millimeters", "mm")]
        for unit in units:
            cursor.execute("INSERT INTO InventoryItemUnit(name, symbol)"
                           " values (?, ?)", unit)
        cursor.execute("CREATE TABLE InventoryItem(itemid INTEGER PRIMARY KEY ASC,"
                       " name, description, unit)")
        connection.commit()
        self.connection = connection

    def fetchall_inventoryitem(self) -> list[InventoryItem]:
        """Get all inventory items from the database."""
        if not self.connection:
            raise RuntimeError("No database open")
        cursor = self.connection.cursor()
        result = []
        for row in cursor.execute("SELECT * FROM InventoryItem"):
            result.append(InventoryItem(*row))
        return result

    def fetchall_inventoryitemunit(self) -> list[InventoryItemUnit]:
        """Get all inventory items from the database."""
        if not self.connection:
            raise RuntimeError("No database open")
        cursor = self.connection.cursor()
        result = []
        for row in cursor.execute("SELECT * FROM InventoryItemUnit"):
            result.append(InventoryItemUnit(*row))
        return result

    def open(self, filename: str) -> None:
        """Open the database."""
        self.connection = sqlite3.connect(filename)
