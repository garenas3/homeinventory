"""Custom widgets for GUI."""
from collections.abc import Callable
from tkinter import ttk


class AddItemWidget(ttk.Frame):
    """A form used to add items to the database.
    
    Use properties to get current user input values. All properties are
    string type. The list of properties corresponding to the user input
    from left to right, top to bottom are:

        name
        unit
        description

    Callbacks are provided as propreties for the buttons. Set them
    as you would any property. The list of callbacks:
        
        on_reset
        on_add

    Example:
        Add the widget to the application.

            widget = AddItemWidget(root)
            widget.grid(column=0, row=0, sticky="ew")

        Update list of units. The `units` dictionary uses the unit name
        as keys and unit ID as values.

            units = {"each": 1, "inches": 2, "feet": 3}
            widget.unit_choices = sorted(units.values())
        
        Use user input values.

            unitid = units[widget.unit]
            database.add_inventoryitem(widget.name, unitid,
                                       widget.description)

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
        self.name_edit = ttk.Entry(self)
        self.name_edit.grid(column=0, row=1, sticky="ew")

        self.unit_label = ttk.Label(self, text="Unit of Measure")
        self.unit_label.grid(column=1, row=0, sticky="w", padx=(5,0))
        self.unit_combobox = ttk.Combobox(self)
        self.unit_combobox.grid(column=1, row=1, sticky="ew", padx=(5,0))

        self.description_label = ttk.Label(self, text="Description")
        self.description_label.grid(column=0, row=3, sticky="w", columnspan=2,
                                    pady=(5,0))
        self.description_edit = ttk.Entry(self)
        self.description_edit.grid(column=0, row=4, sticky="ew", columnspan=2)

        self.button_frame = ttk.Frame(self)
        self.button_frame.grid(row=5, sticky="ew", columnspan=2, pady=10)
        self.button_frame.columnconfigure(0, weight=1)
        self.reset_button = ttk.Button(self.button_frame, text="Reset")
        self.reset_button.grid(column=0, row=0, sticky="e")
        self.add_button = ttk.Button(self.button_frame, text="Add")
        self.add_button.grid(column=1, row=0, sticky="e", padx=(5,0))

    def clear(self) -> None:
        """Clear the contents of all user inputs."""
        self.name_edit.delete(0, "end")
        self.unit_combobox.set("")
        self.description_edit.delete(0, "end")

    @property
    def description(self) -> str:
        """Current text in description field."""
        return self.description_edit.get()

    @property
    def name(self) -> str:
        """Current text in description field."""
        return self.name_edit.get()

    @property
    def on_add(self) -> Callable[[], None]:
        """Add button callback."""
        return self.add_button.invoke

    @on_add.setter
    def on_add(self, value: Callable[[], None]) -> None: 
        """Add button callback."""
        self.add_button.configure(command=value)

    @property
    def on_reset(self) -> Callable[[], None]:
        """Reset button callback."""
        return self.reset_button.invoke

    @on_reset.setter
    def on_reset(self, value: Callable[[], None]) -> None: 
        """Reset button callback."""
        self.reset_button.configure(command=value)

    @property
    def unit(self) -> str:
        """Current text in description field."""
        return self.unit_combobox.get()

    @property
    def unit_choices(self) -> list[str]:
        """Choices for units of measure."""
        return self.unit_combobox.cget("values")

    @unit_choices.setter
    def unit_choices(self, value: list[str]) -> None:
        """Choices for units of measure."""
        self.unit_combobox.configure(values=value)
