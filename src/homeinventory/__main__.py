import argparse
import collections
from collections.abc import Callable
import tkinter as tk
from tkinter import ttk

from .common import InventoryItem


class LineEditWidget:
    """A line edit with a label."""
    def __init__(self, parent, label: str) -> None:
        self._mainframe = ttk.Frame(parent)
        self._mainframe.columnconfigure(0, weight=1)
        self._mainframe.rowconfigure(0, weight=1)
        self._mainframe.rowconfigure(1, weight=1)

        self._label = ttk.Label(self._mainframe, text=label)
        self._label.grid(column=0, row=0, sticky="w")

        self._entry = ttk.Entry(self._mainframe)
        self._entry.grid(column=0, row=1, sticky="ew")

    def grid(self, column: int, row: int, sticky: str,
             columnspan=1) -> None:
        """Placement and behavior on grid."""
        self._mainframe.grid(column=column, row=row, sticky=sticky,
                             columnspan=columnspan)

    @property
    def value(self) -> str:
        """Contents of the text box."""
        return self._entry.get()


class ComboBoxWidget:
    """Choice selection with a label."""
    def __init__(self, parent, label: str) -> None:
        self._mainframe = ttk.Frame(parent)
        self._mainframe.columnconfigure(0, weight=1)
        self._mainframe.rowconfigure(0, weight=1)
        self._mainframe.rowconfigure(1, weight=1)

        self._label = ttk.Label(self._mainframe, text=label)
        self._label.grid(column=0, row=0, sticky="w")

        self._combobox = ttk.Combobox(self._mainframe)
        self._combobox.grid(column=0, row=1, sticky="ew")

        self._choices: list[str] = []

    def grid(self, column: int, row: int, sticky: str) -> None:
        """Placement and behavior on grid."""
        self._mainframe.grid(column=column, row=row, sticky=sticky)

    @property
    def choices(self) -> list[str]:
        """The list of choices."""
        return self._choices.copy()

    @choices.setter
    def choices(self, values: list[str]) -> None:
        """Update the list of choices."""
        self._combobox.configure(values=values)

    @property
    def value(self) -> str:
        """Contents of the text box."""
        return self._combobox.get()


class ButtonWidget:
    """A button with text."""
    def __init__(self, parent, text: str) -> None:
        self._button = ttk.Button(parent, text=text)
        self._command: Callable[[], None] | None = None

    @property
    def command(self) -> Callable[[], None] | None:
        """Callback for button press."""
        return self._command

    @command.setter
    def command(self, value) -> None:
        """Callback for button press."""
        self._command = value
        self._button.configure(command=value)

    def grid(self, column: int, row: int, sticky: str) -> None:
        """Placement and behavior on grid."""
        self._button.grid(column=column, row=row, sticky=sticky)


class ButtonGroupWidget:
    """A group of buttons."""
    def __init__(self, parent) -> None:
        self._mainframe = ttk.Frame(parent)
        self._mainframe.columnconfigure(0, weight=1)
        self._mainframe.rowconfigure(0, weight=1)
        
        self._buttons: dict[str, ButtonWidget] = {}
        self._currentcolumn: int = 0

    def __getitem__(self, key) -> ButtonWidget:
        """Get button with label."""
        if key not in self._buttons:
            self.addbutton(key)
        return self._buttons[key]

    def grid(self, column: int, row: int, sticky: str,
             columnspan=1) -> None:
        """Placement and behavior on grid."""
        self._mainframe.grid(column=column, row=row, sticky=sticky,
                             columnspan=columnspan)

    def addbutton(self, text: str) -> None:
        """Add a button to the group by providing only its text."""
        self._mainframe.columnconfigure(self._currentcolumn+1, weight=0)
        newbutton = ButtonWidget(self._mainframe, text=text)
        newbutton.grid(row=0, column=self._currentcolumn+1, sticky="e")
        self._buttons[text] = newbutton
        self._currentcolumn += 1


class StatusBarWidget:
    """Information about the application."""
    def __init__(self, parent) -> None:
        self._mainframe = ttk.Frame(parent)
        self._mainframe.columnconfigure(0, weight=1)
        self._mainframe.rowconfigure(0, weight=1)

        self._text = ttk.Label(self._mainframe)
        self._text.grid(column=0, row=0, sticky="w")

    def grid(self, column: int, row: int, sticky: str,
             columnspan=1) -> None:
        """Placement and behavior on grid."""
        self._mainframe.grid(column=column, row=row, sticky=sticky,
                             columnspan=columnspan)

    @property
    def text(self) -> str:
        """Current text in the status bar."""
        return self._text.cget("text")

    @text.setter
    def text(self, value) -> None:
        """Update status bar text."""
        self._text.configure(text=value)


class AddItemForm:
    """A form to add items to a database."""
    def __init__(self, parent) -> None:
        self._mainframe = ttk.Frame(parent)
        self._mainframe.columnconfigure(0, weight=1)
        self._mainframe.columnconfigure(1, weight=1)
        self._mainframe.rowconfigure(0, weight=1)
        self._mainframe.rowconfigure(1, weight=1)
        self._mainframe.rowconfigure(2, weight=1)
        self._mainframe.rowconfigure(3, weight=1)

        self._nameinput = LineEditWidget(self._mainframe, "Name")
        self._nameinput.grid(column=0, row=0, sticky="nsew")

        self._unitsselect = ComboBoxWidget(self._mainframe, "Units")
        self._units = {
            "each": ("each", "ea"),
            "inches": ("inches", "in"),
            "feet": ("feet", "ft"),
            }
        self._unitsselect.choices = [key for key in self._units]
        self._unitsselect.grid(column=1, row=0, sticky="nsew")

        self._descriptioninput = LineEditWidget(self._mainframe, "Description")
        self._descriptioninput.grid(column=0, row=1, sticky="ew", columnspan=2)

        self._buttongroup = ButtonGroupWidget(self._mainframe)
        self._buttongroup["Reset"].command = lambda: print("Reset pressed.")
        self._buttongroup["Add"].command = lambda: print("Add pressed.")
        self._buttongroup.grid(column=0, row=2, sticky="ew", columnspan=2)

    def grid(self, column: int, row: int, sticky: str) -> None:
        """Placement and behavior on grid."""
        self._mainframe.grid(column=column, row=row, sticky=sticky)


class Application:
    """Main class to handle GUI."""
    def __init__(self) -> None:
        self._root = tk.Tk()
        self._root.title("Home Inventory")
        self._root.columnconfigure(0, weight=1)
        self._root.rowconfigure(0, weight=1)

        self._mainframe = ttk.Frame(self._root, padding="10 10 10 10")
        self._mainframe.grid(column=0, row=0, sticky="nsew")
        self._mainframe.columnconfigure(0, weight=1)
        self._mainframe.rowconfigure(0, weight=0)

        self._additemform = AddItemForm(self._mainframe)
        self._additemform.grid(column=0, row=0, sticky="nsew")

        self._statusbar = StatusBarWidget(self._mainframe)
        self._statusbar.text = "Ready."
        self._statusbar.grid(column=0, row=3, sticky="ew", columnspan=2)

    def mainloop(self) -> None:
        self._root.mainloop()


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
