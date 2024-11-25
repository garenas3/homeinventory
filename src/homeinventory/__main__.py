import argparse
import tkinter as tk
from tkinter import ttk

from .common import InventoryItem
from .widgets import AddInventoryItem, StatusBar


class Application:
    """Main class to handle GUI."""
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("Home Inventory")
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        self.mainframe = ttk.Frame(self.root, padding="10 10 10 10")
        self.mainframe.grid(column=0, row=0, sticky="nsew")
        self.mainframe.columnconfigure(0, weight=1)
        self.mainframe.rowconfigure(0, weight=0)

        self.additemform = AddInventoryItem(self.mainframe)
        self.additemform.grid(column=0, row=0, sticky="nsew")
        self.additemform.units = ["each", "inches", "feet"]
        self.additemform.default_unit = "each"
        self.additemform.reset()
        def printvalues():
            print(self.additemform.name, self.additemform.unit,
                  self.additemform.description)
        self.additemform.on_add = printvalues

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
