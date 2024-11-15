import csv
from typing import Iterable, Iterator


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


def save(file: str, boxes: Iterable[StringBox]) -> None:
    """Save boxes to a new file.

    Args:
        file: The path of the file to write. An existing file will be
            overwritten.
        boxes: The boxes to write to the file.

    """
    with open(file, "w", newline="") as csvfile:
        boxwriter = csv.writer(csvfile)
        boxwriter.writerow(["Box", "Item"])
        for box in boxes:
            for item in box:
                boxwriter.writerow([box.name, item])


def load(file: str) -> dict[str, StringBox]:
    """Load boxes from a file.

    Args:
        file: The path of the file to read. The file is expected to be
            in CSV format.

    Returns:
        A dictionary of each box read from the file. The name of each
        box is used as the key of each entry. Each entry is a box with
        contents.
    """
    result: dict[str, StringBox] = {}
    with open(file, newline="") as csvfile:
        boxreader = csv.reader(csvfile)
        next(boxreader)  # skip header row
        try:
            for boxname, item in boxreader:
                result.setdefault(boxname, StringBox(boxname)).add(item)
        except ValueError:
            raise ValueError("Error while reading CSV file"
                             f" line {boxreader.line_num}"
                             )
    return result


def search(boxes: Iterable[StringBox], sub: str) -> dict[str, list[str]]:
    """Search for items in a set of boxes.

    Args:
        boxes: A set of boxes to search through.
        sub: The substring to use when performing the search.

    Returns:
        A dictionary of items found in each box that contain the `sub`
        substring. The key of each entry is the name of the box where
        the item was found. The value of each entry is the list of
        items found in a single box. An empty dictionary is returned
        if there were no items found. A dictionary of all the boxes and
        items is returned if `sub` is empty.
    """
    return {box.name: box.search(sub) for box in boxes}
