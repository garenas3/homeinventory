"""Custom widgets for GUI."""
from collections.abc import Callable
import tkinter as tk
from tkinter import ttk

from .common import InventoryItem


class CreateOrUpdateInventoryItemWidget(ttk.Frame):
    """A form used to add items to the database.
    
    Use properties to get current user input values. All properties are
    string type. The list of properties corresponding to the user input
    from left to right, top to bottom are:

        name
        unit
        notes

    Callbacks are provided as propreties for the buttons. Set them
    as you would any property. The list of callbacks:
        
        on_reset
        on_update
        on_create

    Example:
        Add the widget to the application.

            widget = CreateOrUpdateItemWidget(root)
            widget.grid(column=0, row=0, sticky="ew")

        Update list of units. The `units` dictionary uses the unit name
        as keys and unit ID as values.

            units = {"each": 1, "inches": 2, "feet": 3}
            widget.unit_choices = sorted(units.values())
        
        Use user input values.

            unitid = units[widget.unit]
            database.create_inventoryitem(widget.name, unitid,
                                          widget.notes)

        Clear all the fields of the widget.
            
            widget.clear()

        Allow the user to clear whenever the reset button is clicked.

            widget.on_reset = widget.clear
    """
    def __init__(self, parent, **kwargs) -> None:
        super().__init__(parent, **kwargs)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=0)
        self.rowconfigure(2, weight=0)
        self.rowconfigure(3, weight=0)
        self.rowconfigure(4, weight=0)
        self.rowconfigure(5, weight=0)

        self.name_label = ttk.Label(self, text="Name")
        self.name_label.grid(column=0, row=0, sticky="w")
        self.name_input = ttk.Entry(self)
        self.name_input.grid(column=0, row=1, sticky="ew")

        self.unit_label = ttk.Label(self, text="Unit of Measure")
        self.unit_label.grid(column=1, row=0, sticky="w", padx=(5,0))
        self.unit_combobox = ttk.Combobox(self)
        self.unit_combobox.grid(column=1, row=1, sticky="ew", padx=(5,0))

        self.notes_label = ttk.Label(self, text="Notes")
        self.notes_label.grid(column=0, row=3, sticky="w", columnspan=2,
                                    pady=(5,0))
        self.notes_input = ttk.Entry(self)
        self.notes_input.grid(column=0, row=4, sticky="ew", columnspan=2)

        self.button_frame = ttk.Frame(self)
        self.button_frame.grid(row=5, sticky="ew", columnspan=2, pady=10)
        self.button_frame.columnconfigure(0, weight=1)
        self.reset_button = ttk.Button(self.button_frame, text="Reset")
        self.reset_button.grid(column=0, row=0, sticky="w")
        self.update_button = ttk.Button(self.button_frame, text="Update")
        self.update_button.grid(column=1, row=0, sticky="e", padx=(5,0))
        self.create_button = ttk.Button(self.button_frame, text="Create")
        self.create_button.grid(column=2, row=0, sticky="e", padx=(5,0))

    def clear(self) -> None:
        """Clear the contents of all user inputs."""
        self.name_input.delete(0, "end")
        self.unit_combobox.set("")
        self.notes_input.delete(0, "end")

    @property
    def name(self) -> str:
        """Current text in name field."""
        return self.name_input.get()

    @name.setter
    def name(self, value) -> None:
        """Current text in name field."""
        self.name_input.delete(0, "end")
        self.name_input.insert(0, value)

    @property
    def notes(self) -> str:
        """Current text in notes field."""
        return self.notes_input.get()

    @notes.setter
    def notes(self, value: str) -> None:
        """Current text in notes field."""
        self.notes_input.delete(0, "end")
        self.notes_input.insert(0, value)

    @property
    def unit(self) -> str:
        """Current text in unit field."""
        return self.unit_combobox.get()

    @unit.setter
    def unit(self, value: str) -> None:
        """Current text in unit field."""
        self.unit_combobox.delete(0, "end")
        self.unit_combobox.insert(0, value)

    @property
    def unit_choices(self) -> list[str]:
        """Choices for units of measure."""
        return self.unit_combobox.cget("values")

    @unit_choices.setter
    def unit_choices(self, value: list[str]) -> None:
        """Choices for units of measure."""
        self.unit_combobox.configure(values=value)

    @property
    def on_create(self) -> Callable[[], None]:
        """Create button callback."""
        return self.create_button.invoke

    @on_create.setter
    def on_create(self, value: Callable[[], None]) -> None: 
        """Create button callback."""
        self.create_button.configure(command=value)

    @property
    def on_reset(self) -> Callable[[], None]:
        """Reset button callback."""
        return self.reset_button.invoke

    @on_reset.setter
    def on_reset(self, value: Callable[[], None]) -> None: 
        """Reset button callback."""
        self.reset_button.configure(command=value)

    @property
    def on_update(self) -> Callable[[], None]:
        """Update button callback."""
        return self.update_button.invoke

    @on_update.setter
    def on_update(self, value: Callable[[], None]) -> None: 
        """Update button callback."""
        self.update_button.configure(command=value)


class InventoryItemView(ttk.Frame):
    """View and select inventory items."""
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=0)
        self.rowconfigure(0, weight=1)

        self.view = ttk.Treeview(self)
        self.view["show"] = "headings"
        self.view["columns"] = ["Name","Unit","Notes"]
        self.view.heading("Name", text="Name")
        self.view.heading("Unit", text="Unit")
        self.view.heading("Notes", text="Notes")
        self.view.column("Name", width=100)
        self.view.column("Unit", width=100)
        self.view.grid(column=0, row=0, sticky="nsew")


        self.scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL,
                                       command=self.view.yview)
        self.scrollbar.grid(column=1, row=0, sticky="ns")

        self.view["yscrollcommand"] = self.scrollbar.set

        self._on_select: Callable[[], None] = lambda: None

    def refresh(self, items: list[InventoryItem]) -> None:
        """Refresh the list of items by name in ascending order."""
        self.view.delete(*self.view.get_children())
        for item in sorted(items, key=lambda item: item.name):
            self.view.insert("", "end", item.itemid,
                             values=(item.name,item.unit.name,item.notes))

    def clear_selection(self)-> None:
        """Clear current selection."""
        if not self.current_itemid:
            return
        self.view.selection_remove(self.view.selection()[0])

    @property
    def current_itemid(self) -> int:
        """Current selected itemid."""
        selection_tuple = self.view.selection()
        if not selection_tuple:
            return 0
        return int(selection_tuple[0])

    @property
    def on_select(self) -> Callable[[], None]:
        """Selection changed callback."""
        return self._on_select

    @on_select.setter
    def on_select(self, value: Callable[[], None]) -> None:
        """Selection changed callback."""
        self._on_select = value
        self.view.bind("<<TreeviewSelect>>", lambda _: value())
