from dataclasses import dataclass


@dataclass
class InventoryItemUnit:
    """Unit of measure for an item."""
    name: str
    symbol: str


@dataclass
class InventoryItem:
    """Attributes to describe an item."""
    itemid: int
    name: str
    description: str
    unit: InventoryItemUnit


@dataclass
class InventoryItemGroup:
    """Metadata for a items in a box."""
    item: InventoryItem
    quantity: float


class InventoryItemBox:
    """A collection of items stored in a box."""
    pass
