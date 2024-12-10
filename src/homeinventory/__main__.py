import argparse
import tkinter as tk
from tkinter import ttk

from .common import InventoryItem, InventoryItemUnit
from .database import InventoryDatabase
from .widgets import AddInventoryItem, InventoryItemListView, StatusBar


class Application:
    """Main class to handle GUI."""
    def __init__(self) -> None:
        self.database = InventoryDatabase(":memory:")
        self.units: dict[str, InventoryItemUnit] = {
            u.name: u for u in self.database.fetchall_inventoryitemunit()
        }

        self.root = tk.Tk()
        self.root.title("Home Inventory")
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        self.mainframe = ttk.Frame(self.root, padding="10 10 10 10")
        self.mainframe.grid(column=0, row=0, sticky="nsew")
        self.mainframe.columnconfigure(0, weight=1)
        self.mainframe.rowconfigure(0, weight=0)
        self.mainframe.rowconfigure(1, weight=1)

        self.additemform = AddInventoryItem(self.mainframe)
        self.additemform.grid(column=0, row=0, sticky="nsew")
        self.additemform.units = [u for u in sorted(self.units.keys())]
        self.additemform.default_unit = "each"
        self.additemform.reset()

        self.inventoryitemview = InventoryItemListView(self.mainframe, "Items")
        self.inventoryitemview.grid(column=0, row=1, sticky="ew")

        def addinventoryitem():
            self.database.add_inventoryitem(
                self.additemform.name,
                self.units[self.additemform.unit].unitid,
                self.additemform.description)
            self.inventoryitemview.clear()
            for item in self.database.fetchall_inventoryitem():
                self.inventoryitemview.append(item)
        self.additemform.on_add = addinventoryitem

        self.statusbar = StatusBar(self.mainframe)
        self.statusbar.text = "Ready."
        self.statusbar.grid(column=0, row=3, sticky="ew", columnspan=2)

    def mainloop(self) -> None:
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
