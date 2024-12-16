"""Common home inventory classes and functions."""
from dataclasses import dataclass


@dataclass
class InventoryItemUnit:
    """Unit of measure for an item."""
    unitid: int
    name: str
    symbol: str


@dataclass
class InventoryItem:
    """Attributes to describe an item."""
    itemid: int
    name: str
    unit: InventoryItemUnit
    notes: str


class InventoryItemBox:
    """A collection of items stored in a box."""
    def __init__(self) -> None:
        pass
