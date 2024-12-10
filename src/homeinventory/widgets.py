"""Custom widgets for GUI."""
from collections.abc import Callable
from tkinter import ttk

from .common import InventoryItem


class LineEdit:
    """A line edit with a label.

    A line edit is a text box that accepts a single line of input. A
    label above the text box gives the line edit a name and helps the
    user identify its purpose.

    Example:
        Create a line edit with the label "Name".

            self.mainframe = ttk.Frame(parent)
            self.nameinput = LineEdit(self.mainframe, "Name")
            self.nameinput.grid(column=0, row=0, sticky="nsew")

        Use the `value` property to get the current input text.
            
            name = self.nameinput.value
    """
    def __init__(self, parent, labeltext: str) -> None:
        self.mainframe = ttk.Frame(parent)
        self.mainframe.columnconfigure(0, weight=1)
        self.mainframe.rowconfigure(0, weight=1)
        self.mainframe.rowconfigure(1, weight=1)

        self.label = ttk.Label(self.mainframe, text=labeltext)
        self.label.grid(column=0, row=0, sticky="w")

        self.entry = ttk.Entry(self.mainframe)
        self.entry.grid(column=0, row=1, sticky="ew")

    def clear(self) -> None:
        """Clear the current text from the line edit."""
        self.entry.delete(0, "end")

    def focus(self) -> None:
        """Return focus to this widget."""
        self.entry.focus_set()

    def grid(self, column: int, row: int, sticky: str, columnspan=1) -> None:
        """Placement and behavior on grid."""
        self.mainframe.grid(column=column, row=row, sticky=sticky,
                            columnspan=columnspan)

    @property
    def value(self) -> str:
        """Contents of the text box."""
        return self.entry.get()


class ComboBox:
    """Choice selection with a label.

    A combo box features a drop down containing a list of items. One of
    the items can be selected. If an item is not on the list, the user
    can use the line edit to enter custom text instead if allowed.

    Example:
        Create a combo box with the label "Unit".

            self.mainframe = ttk.Frame(parent)
            self.unitselect = ComboBox(self.mainframe, "Unit")
            self.unitselect.grid(column=1, row=0, sticky="nsew")

        The list of items can be updated using the `choices` property.

            self.units = {
                "each": ("each", "ea"),
                "inches": ("inches", "in"),
                "feet": ("feet", "ft"),
                }
            self.unitselect.choices = [key for key in self.units]

        Use the `value` property to get the current selection.

            unit = self.unitselected.value
    """
    def __init__(self, parent, labeltext: str) -> None:
        self.mainframe = ttk.Frame(parent)
        self.mainframe.columnconfigure(0, weight=1)
        self.mainframe.rowconfigure(0, weight=1)
        self.mainframe.rowconfigure(1, weight=1)

        self.label = ttk.Label(self.mainframe, text=labeltext)
        self.label.grid(column=0, row=0, sticky="w")

        self.combobox = ttk.Combobox(self.mainframe)
        self.combobox.grid(column=0, row=1, sticky="ew")

        self._choices: list[str] = []

    def grid(self, column: int, row: int, sticky: str) -> None:
        """Placement and behavior on grid."""
        self.mainframe.grid(column=column, row=row, sticky=sticky)

    @property
    def choices(self) -> list[str]:
        """The list of choices."""
        return self._choices.copy()

    @choices.setter
    def choices(self, values: list[str]) -> None:
        """Update the list of choices."""
        self._choices = values
        self.combobox.configure(values=values)

    @property
    def value(self) -> str:
        """Contents of the text box."""
        return self.combobox.get()

    @value.setter
    def value(self, value: str) -> None:
        """Set the value of the combo box.

        Raises:
            ValueError: if value is not in list of choices.
        """
        self.combobox.current(self._choices.index(value))


class Button:
    """A button with text.
    
    A button can be clicked by the user to initiate a command. A
    command can be either a function or lambda with no arguments.

    Example:
        Create a submit button.

            self.mainframe = ttk.Frame(parent)
            submitbutton = Button(self.mainframe, text="Submit")
            submitbutton.grid(row=0, column=1, sticky="e")

        By assigning a lambda to the `command` property, clicking the
        button will print "Form submitted!" to the console in the
        following example.

            submitbutton.command = lambda: print("Form submitted!")
    """
    def __init__(self, parent, text: str) -> None:
        self.button = ttk.Button(parent, text=text)
        self._command: Callable[[], None] | None = None

    @property
    def command(self) -> Callable[[], None] | None:
        """Callback for button press."""
        return self._command

    @command.setter
    def command(self, value: Callable[[], None]) -> None:
        """Callback for button press."""
        self._command = value
        self.button.configure(command=value)

    def grid(self, column: int, row: int, sticky: str) -> None:
        """Placement and behavior on grid."""
        self.button.grid(column=column, row=row, sticky=sticky)


class ButtonGroup:
    """A group of buttons.

    A button group makes it easier to manage a set of buttons in some
    section of the window.

    Example:
        Create and manage buttons by passing button text as a key to
        the button group. Buttons require a command to be useful. The
        `command` property of a new button can be assigned immediately.

            self.mainframe = ttk.Frame(parent)
            self.btngrp = ButtonGroup(self.mainframe)
            self.btngrp["Reset"].command = lambda: print("Reset pressed.")
            self.btngrp["Add"].command = lambda: print("Add pressed.")
            self.btngrp.grid(column=0, row=2, sticky="ew", columnspan=2)
    """
    def __init__(self, parent) -> None:
        self.mainframe = ttk.Frame(parent)
        self.mainframe.columnconfigure(0, weight=1)
        self.mainframe.rowconfigure(0, weight=1)
        
        self.buttons: dict[str, Button] = {}
        self.currentcolumn: int = 0

    def __getitem__(self, key) -> Button:
        """Get button with label."""
        if key not in self.buttons:
            self.addbutton(key)
        return self.buttons[key]

    def grid(self, column: int, row: int, sticky: str, columnspan=1) -> None:
        """Placement and behavior on grid."""
        self.mainframe.grid(column=column, row=row, sticky=sticky,
                             columnspan=columnspan)

    def addbutton(self, text: str) -> None:
        """Add a button to the group by providing only its text."""
        self.mainframe.columnconfigure(self.currentcolumn+1, weight=0)
        newbutton = Button(self.mainframe, text=text)
        newbutton.grid(row=0, column=self.currentcolumn+1, sticky="e")
        self.buttons[text] = newbutton
        self.currentcolumn += 1


class StatusBar:
    """Information about the application.

    A status bar is typically located at the bottom of a window. Text is
    displayed notifying the user the current state of the application or
    of a recent change that occurred.

    Example:
        Adding a status bar to a window is straighforward. A status bar
        will most likely located in the last row.

            self.mainframe = ttk.Frame(self.root)
            self.sbar = StatusBar(self.mainframe)
            self.sbar.text = "Ready."
            self.sbar.grid(column=0, row=3, sticky="ew", columnspan=2)
    """
    def __init__(self, parent) -> None:
        self.mainframe = ttk.Frame(parent)
        self.mainframe.columnconfigure(0, weight=1)
        self.mainframe.rowconfigure(0, weight=1)

        self._text = ttk.Label(self.mainframe)
        self._text.grid(column=0, row=0, sticky="w")

    def grid(self, column: int, row: int, sticky: str,
             columnspan=1) -> None:
        """Placement and behavior on grid."""
        self.mainframe.grid(column=column, row=row, sticky=sticky,
                            columnspan=columnspan)

    @property
    def text(self) -> str:
        """Current text in the status bar."""
        return self._text.cget("text")

    @text.setter
    def text(self, value: str) -> None:
        """Update status bar text."""
        self._text.configure(text=value)


class AddInventoryItem:
    """Add items to a database."""
    def __init__(self, parent) -> None:
        self.mainframe = ttk.Frame(parent)
        self.mainframe.columnconfigure(0, weight=1)
        self.mainframe.columnconfigure(1, weight=1)
        self.mainframe.rowconfigure(0, weight=1)
        self.mainframe.rowconfigure(1, weight=1)
        self.mainframe.rowconfigure(2, weight=1)
        self.mainframe.rowconfigure(3, weight=1)

        self.nameinput = LineEdit(self.mainframe, "Name")
        self.nameinput.grid(column=0, row=0, sticky="nsew")

        self.unitselect = ComboBox(self.mainframe, "Unit")
        self.unitselect.grid(column=1, row=0, sticky="nsew")

        self.descriptioninput = LineEdit(self.mainframe, "Description")
        self.descriptioninput.grid(column=0, row=1, sticky="ew", columnspan=2)

        self.buttongroup = ButtonGroup(self.mainframe)
        self.buttongroup["Reset"].command = self.reset
        self.buttongroup["Add"].command = lambda: print("Add pressed.")
        self.buttongroup.grid(column=0, row=2, sticky="ew", columnspan=2)

        self.default_unit: str = ""

    @property
    def description(self) -> str:
        """The current text in the description input."""
        return self.descriptioninput.value

    @property
    def name(self) -> str:
        """The current text in the name input."""
        return self.nameinput.value

    @property
    def on_add(self) -> Callable[[], None] | None:
        """The callback used for the "Add" button."""
        return self.buttongroup["Add"].command

    @on_add.setter
    def on_add(self, value: Callable[[], None]) -> None:
        """The "Add" button callback."""
        self.buttongroup["Add"].command = value

    def grid(self, column: int, row: int, sticky: str) -> None:
        """Placement and behavior on grid."""
        self.mainframe.grid(column=column, row=row, sticky=sticky)

    def reset(self) -> None:
        """Reset the fields to their default or empty values."""
        self.nameinput.clear()
        self.unitselect.value = self.default_unit
        self.descriptioninput.clear()
        self.nameinput.focus()

    @property
    def unit(self) -> str:
        """The current text in the unit combo box."""
        return self.unitselect.value

    @property
    def units(self) -> list[str]:
        """The list of units last assigned to the widget."""
        return self.unitselect.choices

    @units.setter
    def units(self, value: list[str]) -> None:
        """Update the list of units."""
        self._units = value
        self.unitselect.choices = value


class InventoryItemListView:
    """View the inventory items added to the database."""
    def __init__(self, parent, labeltext: str) -> None:
        self.mainframe = ttk.Frame(parent)
        self.mainframe.columnconfigure(0, weight=1)
        self.mainframe.rowconfigure(0, weight=1)
        self.mainframe.rowconfigure(1, weight=1)

        self.label = ttk.Label(self.mainframe, text=labeltext)
        self.label.grid(column=0, row=0, sticky="w")

        self.listview = ttk.Treeview(self.mainframe, show="tree")
        self.listview.grid(column=0, row=1, sticky="ew")

        self.inventoryitems: list[InventoryItem] = []

    def append(self, inventoryitem: InventoryItem) -> None:
        """Add an item to the list."""
        self.listview.insert("", "end", inventoryitem.itemid, text=inventoryitem.name)
        self.inventoryitems.append(inventoryitem)

    def clear(self) -> None:
        """Clear the list of all items."""
        for inventoryitem in self.inventoryitems:
            self.listview.delete(inventoryitem.itemid)

    def grid(self, column: int, row: int, sticky: str, columnspan=1) -> None:
        """Placement and behavior on grid."""
        self.mainframe.grid(column=column, row=row, sticky=sticky,
                            columnspan=columnspan)
