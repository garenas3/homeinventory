import argparse
import sqlite3
import tkinter as tk
from tkinter import ttk

from . import database
from .common import InventoryItem, InventoryItemUnit
from .widgets import AddItemWidget


class NoDatabaseConnectionError(Exception):
    pass


class Application:
    """Main class to handle GUI."""
    def __init__(self) -> None:
        self.setup_ui()
        
        self.connection: sqlite3.Connection | None  = None
        self.units: list[InventoryItemUnit] = []
        self.items: list[InventoryItem] = []

        self.init_inmemory_database()
        self.init_units()
        self.init_additemwidget()
        self.refresh_itemview()

    def setup_ui(self) -> None:
        """Set up the user interface."""
        self.root = tk.Tk()
        self.root.title("Home Inventory")
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        style = ttk.Style()
        style.theme_use("alt")

        self.mainframe = ttk.Frame(self.root, padding="10 10 10 10")
        self.mainframe.grid(column=0, row=0, sticky="nsew")
        self.mainframe.columnconfigure(0, weight=1)
        self.mainframe.rowconfigure(0, weight=1)
        self.mainframe.rowconfigure(1, weight=0)

        self.itemviewframe = ttk.Labelframe(self.mainframe, text="Item View")
        self.itemviewframe.columnconfigure(0, weight=1)
        self.itemviewframe.rowconfigure(0, weight=1)
        self.itemviewframe.grid(column=0, row=0, sticky="nsew", pady=(5, 0))
        self.itemviewwidget = ttk.Treeview(self.itemviewframe, show="headings",
                                           columns=["Name", "Unit", "Description"])
        self.itemviewwidget.heading("Name", text="Name")
        self.itemviewwidget.heading("Unit", text="Unit")
        self.itemviewwidget.heading("Description", text="Description")
        self.itemviewwidget.grid(column=0, row=0, sticky="nsew", padx=10,
                                 pady=(5, 10))

        self.additemframe = ttk.Labelframe(self.mainframe, text="Add Item")
        self.additemframe.columnconfigure(0, weight=1)
        self.additemframe.rowconfigure(0, weight=1)
        self.additemframe.grid(column=0, row=1, sticky="ew")
        self.additemwidget = AddItemWidget(self.additemframe)
        self.additemwidget.grid(column=0, row=0, sticky="ew", padx=10,
                                pady=(5,10))
        self.additemwidget.on_reset = self.reset_additemwidget
        self.additemwidget.on_add = self.additem

    def init_inmemory_database(self) -> None:
        """Initialize an in-memory database."""
        self.connection = sqlite3.Connection(":memory:")
        database.initialize(self.connection)

    def init_units(self) -> None:
        """Initialize the `units` member."""
        if not self.connection:
            raise NoDatabaseConnectionError
        self.units = database.fetchall_inventoryitemunit(self.connection)

    def init_additemwidget(self) -> None:
        """Initialize the `AddItemWidget`."""
        self.additemwidget.unit_choices = sorted(unit.name
                                                 for unit in self.units)
        self.reset_additemwidget()

    def reset_additemwidget(self) -> None:
        """Reset the `AddItemWidget`."""
        self.additemwidget.clear()
        self.additemwidget.unit_combobox.set(self.units[0].name)

    def additem(self) -> None:
        """Add an item to the database."""
        if not self.additemwidget.name:
            return
        if not self.connection:
            raise NoDatabaseConnectionError
        units = {unit.name: unit for unit in self.units}
        name = self.additemwidget.name
        unit = units[self.additemwidget.unit]
        description = self.additemwidget.description
        itemid = database.add_inventoryitem(self.connection, name, unit.unitid,
                                            description)
        self.items.append(InventoryItem(itemid, name, unit, description))
        self.refresh_itemview()
        self.reset_additemwidget()

    def refresh_itemview(self) -> None:
        """Refresh the item view."""
        self.itemviewwidget.delete(*self.itemviewwidget.get_children())
        for item in self.items:
            self.itemviewwidget.insert("", "end", item.itemid,
                                       values=(item.name, item.unit.name,
                                               item.description))

    def mainloop(self) -> None:
        """Start the program loop."""
        self.root.mainloop()


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="homeinventory",
        description="Manage a home inventory."
        )
    parser.add_argument("filename")

    app = Application()
    app.mainloop()


if __name__ == "__main__":
    main()
