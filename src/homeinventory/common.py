import csv
from dataclasses import dataclass
from typing import Iterable

from .stringbox import StringBox


@dataclass
class Item:
    """Attributes to describe an item."""
    itemid: int
    name: str


def exportcsv(file: str, boxes: Iterable[StringBox]) -> None:
    """Save boxes to a new CSV file.

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


def importcsv(file: str) -> dict[str, StringBox]:
    """Load boxes from a CSV file.

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
                             f" line {boxreader.line_num}")
    return result


def searchboxes(boxes: Iterable[StringBox], sub: str) -> dict[str, list[str]]:
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
    result = {box.name: box.search(sub) for box in boxes}
    return {key: value for key, value in result.items() if value} 
