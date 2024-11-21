"""Manage a home inventory.

Import the project to begin.

>>> import homeinventory
>>> from homeinventory import StringBox

Create a box with a useful naming convention. For example, consider
using a short description of the contents of each box.

>>> woodtools_box = StringBox("Wood Tools")
>>> cutlery_box = StringBox("Cutlery")

Or, use some sort of smart identifier.

>>> a1_box = StringBox("A1")
>>> a2_box = StringBox("A2")
>>> b1_box = StringBox("B1")

The rest of this guide uses boxes containing food. Create an empty box
by providing only the name.

>>> fruit_box = StringBox("Fruit")

A box can be intialized with contents if desired.

>>> nuts_box = StringBox("Nuts", ["Almonds", "Cashews", "Hazelnuts"])

Add contents to a box one at a times using the `add` method.

>>> fruit_box.add("Apples")
>>> fruit_box.add("Apricots")
>>> fruit_box.add("Hazelnuts")
>>> fruit_box.add("Raspberries")
>>> fruit_box.add("Strawberries")

Use the `remove` method to remove a single item from the box.

>>> fruit_box.remove("Apricots")  # doctest:+ELLIPSIS
>>> fruit_box
StringBox(name='Fruit', items=['Apples', 'Hazelnuts', ...])

To search for items, use the `search` method. This method performs a
case-insensitive search.

>>> fruit_box.search("berries")
['Raspberries', 'Strawberries']

The module level search method can be used to search multiple boxes at
once.

>>> homeinventory.searchboxes([fruit_box, nuts_box], "hazelnuts")
{'Fruit': ['Hazelnuts'], 'Nuts': ['Hazelnuts']}

For a home inventory system like this to be useful, it must be saved to
a file. Save the information to a CSV file using the `exportcsv`
function.

>>> homeinventory.exportcsv(  # doctest:+SKIP
...     "inventory.csv", 
...     [fruit_box, nuts_box]
... )

Use the `load` function to resume working at a later date.

>>> inventory = homeinventory.importcsv("inventory.csv")  # doctest:+SKIP
>>> inventory  # doctest:+SKIP
{'Fruit': StringBox(name='Fruit', items=[...]), 'Nuts': StringBox(...)}
"""
from .stringboxutil import exportcsv
from .stringboxutil import importcsv
from .stringboxutil import searchboxes
from .stringbox import StringBox


__all__ = [
    "StringBox",
    "exportcsv",
    "importcsv",
    "searchboxes",
]
