import argparse
import tkinter as tk
from tkinter import ttk
from typing import Iterable

from .common import importcsv
from .stringbox import StringBox


class Application:
    def __init__(self) -> None:
        self._root = tk.Tk()
        self._root.title("Home Inventory")
        self._root.columnconfigure(0, weight=1)
        self._root.rowconfigure(0, weight=1)
        self._mainframe = ttk.Frame(self._root, padding="10 10 10 10")
        self._mainframe.grid(column=0, row=0, sticky="nesw")
        self._mainframe.columnconfigure(0, weight=1)
        self._mainframe.rowconfigure(0, weight=1)
        self._boxview = ttk.Treeview(self._mainframe, show="tree")
        self._boxview.grid(column=0, row=0, sticky="nesw")

    def displayboxes(self, boxes: Iterable[StringBox]) -> None:
        for box in boxes:
            boxid = self._boxview.insert("", "end", text=box.name)
            for item in box:
                self._boxview.insert(boxid, "end", text=item)

    def mainloop(self) -> None:
        self._root.mainloop()


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="homeinventory",
        description="Manage a home inventory."
        )
    parser.add_argument("filename")
    args = parser.parse_args()
    boxes = importcsv(args.filename)

    app = Application()
    app.displayboxes(boxes.values())
    app.mainloop()


if __name__ == "__main__":
    main()
