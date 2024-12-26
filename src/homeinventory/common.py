"""Common home inventory classes and functions."""
from dataclasses import dataclass


@dataclass(frozen=True)
class InventoryItemUnit:
    """Unit of measure for an item."""
    unitid: int
    name: str
    symbol: str


@dataclass(frozen=True)
class InventoryItem:
    """Attributes to describe an item."""
    itemid: int
    name: str
    unit: InventoryItemUnit
    notes: str
