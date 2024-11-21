from dataclasses import dataclass


@dataclass
class Item:
    """Attributes to describe an item."""
    itemid: int
    name: str
