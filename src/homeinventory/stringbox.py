from typing import Iterator


class StringBox:
    """A collection of items to store in a box.

    Examples:
        Create an empty box.

        >>> fruit_box = StringBox("Fruits")
        >>> fruit_box
        StringBox(name='Fruits', items=[])

        Create a box with pre-existing items.

        >>> nut_box = StringBox("Nuts", ["Almonds", "Cashews"])
        >>> nut_box
        StringBox(name='Nuts', items=['Almonds', 'Cashews'])

        Add items to a box.

        >>> fruit_box.add("Apples")
        >>> fruit_box.add("Blueberries")
        >>> fruit_box
        StringBox(name='Fruits', items=['Apples', 'Blueberries'])

        """

    def __init__(self, name: str, items: list[str] = []) -> None:
        """Create a named box."""
        self.name = name
        self._items = items.copy()

    def __iter__(self) -> Iterator[str]:
        """Return an iterator for the items in the box."""
        return iter(self._items)

    def __len__(self) -> int:
        """Return the number of items in the box."""
        return len(self._items)

    def __repr__(self) -> str:
        """Return a string representation of the box."""
        return f"StringBox(name={self.name!r}, items={self._items!r})"

    def add(self, item: str) -> None:
        """Add an item to the box."""
        self._items.append(item)

    def remove(self, item: str) -> None:
        """Remove an item from the box."""
        self._items.remove(item)

    def search(self, sub: str) -> list[str]:
        """Perform a case-insensitive search on items in the box.

        Args:
            sub: The substring to use when performing the search.

        Returns:
            A list of items that contain the `sub` substring. An empty
            list is returned if no items contain the substring. A list
            of all the items are returned if `sub` is empty.
        """
        result = []
        for item in self._items:
            if sub.lower() in item.lower():
                result.append(item)
        return result
