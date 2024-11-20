import argparse
from collections.abc import Callable
import tkinter as tk
from tkinter import ttk

from .common import importcsv, searchboxes
from .stringbox import StringBox


class SearchWidget(ttk.Frame):
    on_submit: Callable[[str], None]

    def __init__(self, master=None, **kwargs) -> None:
        super().__init__(master, **kwargs)
        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=0)
        self.rowconfigure(0, weight=1)

        self._search_label = ttk.Label(self, text="Search")
        self._search_label.grid(column=0, row=0, sticky="e")

        self._search_entry = ttk.Entry(self)
        self._search_entry.grid(column=1, row=0, sticky="ew")
        self._search_entry.bind('<Return>', lambda _: self._on_submit())

        self._submit_button = ttk.Button(self, text="Submit")
        self._submit_button.grid(column=2, row=0)
        self._submit_button.configure(command=self._on_submit)

    def _on_submit(self) -> None:
        self.on_submit(self._search_entry.get())


class Application:
    boxes: dict[str, StringBox] = {}

    def __init__(self) -> None:
        self._root = tk.Tk()
        self._root.title("Home Inventory")
        self._root.columnconfigure(0, weight=1)
        self._root.rowconfigure(0, weight=1)

        self._mainframe = ttk.Frame(self._root, padding="10 10 10 10")
        self._mainframe.grid(column=0, row=0, sticky="nsew")
        self._mainframe.columnconfigure(0, weight=1)
        self._mainframe.rowconfigure(0, weight=0)
        self._mainframe.rowconfigure(1, weight=1)

        self._searchwidget = SearchWidget(self._mainframe, padding="0 0 0 5")
        self._searchwidget.grid(column=0, row=0, sticky="ew")
        self._searchwidget.on_submit = self.displayboxes

        self._boxview = ttk.Treeview(self._mainframe, show="tree")
        self._boxview.grid(column=0, row=1, sticky="nsew")

    def displayboxes(self, itemfilter: str = "") -> None:
        for child in self._boxview.get_children():
            self._boxview.delete(child)
        boxes = searchboxes(self.boxes.values(), itemfilter)
        for boxname, box in boxes.items():
            boxid = self._boxview.insert("", "end", text=boxname)
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

    app = Application()
    app.boxes = importcsv(args.filename)
    app.displayboxes()
    app.mainloop()


if __name__ == "__main__":
    main()
