from dataclasses import dataclass


@dataclass
class InventoryItem:
    """Attributes to describe an item."""
    itemid: int
    name: str


@dataclass
class InventoryItemGroup:
    """Metadata for a items in a box."""
    pass


class InventoryItemBox:
    """A collection of items stored in a box."""
    pass
