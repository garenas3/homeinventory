"""Custom widgets for GUI."""
from collections.abc import Callable
from tkinter import ttk


class LineEdit:
    """A line edit with a label."""
    def __init__(self, parent, label: str) -> None:
        self.mainframe = ttk.Frame(parent)
        self.mainframe.columnconfigure(0, weight=1)
        self.mainframe.rowconfigure(0, weight=1)
        self.mainframe.rowconfigure(1, weight=1)

        self.label = ttk.Label(self.mainframe, text=label)
        self.label.grid(column=0, row=0, sticky="w")

        self.entry = ttk.Entry(self.mainframe)
        self.entry.grid(column=0, row=1, sticky="ew")

    def grid(self, column: int, row: int, sticky: str,
             columnspan=1) -> None:
        """Placement and behavior on grid."""
        self.mainframe.grid(column=column, row=row, sticky=sticky,
                            columnspan=columnspan)

    @property
    def value(self) -> str:
        """Contents of the text box."""
        return self.entry.get()


class ComboBox:
    """Choice selection with a label."""
    def __init__(self, parent, label: str) -> None:
        self.mainframe = ttk.Frame(parent)
        self.mainframe.columnconfigure(0, weight=1)
        self.mainframe.rowconfigure(0, weight=1)
        self.mainframe.rowconfigure(1, weight=1)

        self.label = ttk.Label(self.mainframe, text=label)
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
        self.combobox.configure(values=values)

    @property
    def value(self) -> str:
        """Contents of the text box."""
        return self.combobox.get()


class Button:
    """A button with text."""
    def __init__(self, parent, text: str) -> None:
        self.button = ttk.Button(parent, text=text)
        self._command: Callable[[], None] | None = None

    @property
    def command(self) -> Callable[[], None] | None:
        """Callback for button press."""
        return self._command

    @command.setter
    def command(self, value) -> None:
        """Callback for button press."""
        self._command = value
        self.button.configure(command=value)

    def grid(self, column: int, row: int, sticky: str) -> None:
        """Placement and behavior on grid."""
        self.button.grid(column=column, row=row, sticky=sticky)


class ButtonGroup:
    """A group of buttons."""
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

    def grid(self, column: int, row: int, sticky: str,
             columnspan=1) -> None:
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
    """Information about the application."""
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
    def text(self, value) -> None:
        """Update status bar text."""
        self._text.configure(text=value)


class AddInventoryItem:
    """A form to add items to a database."""
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

        self.unitsselect = ComboBox(self.mainframe, "Units")
        self.units = {
            "each": ("each", "ea"),
            "inches": ("inches", "in"),
            "feet": ("feet", "ft"),
            }
        self.unitsselect.choices = [key for key in self.units]
        self.unitsselect.grid(column=1, row=0, sticky="nsew")

        self.descriptioninput = LineEdit(self.mainframe, "Description")
        self.descriptioninput.grid(column=0, row=1, sticky="ew", columnspan=2)

        self.buttongroup = ButtonGroup(self.mainframe)
        self.buttongroup["Reset"].command = lambda: print("Reset pressed.")
        self.buttongroup["Add"].command = lambda: print("Add pressed.")
        self.buttongroup.grid(column=0, row=2, sticky="ew", columnspan=2)

    def grid(self, column: int, row: int, sticky: str) -> None:
        """Placement and behavior on grid."""
        self.mainframe.grid(column=column, row=row, sticky=sticky)
