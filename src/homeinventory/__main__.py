import argparse
import sqlite3
import tkinter as tk
from tkinter import ttk

from . import database
from .common import InventoryItem, InventoryItemUnit
from .widgets import CreateOrUpdateInventoryItemWidget, InventoryItemView


class NoDatabaseConnectionError(Exception):
    pass


class InventoryDatabase():
    def __init__(self) -> None:
        self.connection: sqlite3.Connection | None  = None
        self.units: list[InventoryItemUnit] = []
        self.units_by_id: dict[int, InventoryItemUnit] = {}
        self.units_by_name: dict[str, InventoryItemUnit] = {}
        self.default_unit_name: str = ""
        self.items: list[InventoryItem] = []
        self.items_by_id: dict[int, InventoryItem] = {}

        self.init_inmemory_database()
        self.init_units()
        self.init_items()

    def init_inmemory_database(self) -> None:
        """Initialize an in-memory database."""
        self.connection = sqlite3.Connection(":memory:")
        database.initialize(self.connection)
        
        for i in range(100):
            database.create_inventoryitem(self.connection,
                f"Item {i+1:03}", 1, f"Test item {i+1}")

    def init_units(self) -> None:
        """Initialize the `units` member."""
        if not self.connection:
            raise NoDatabaseConnectionError
        self.units = database.fetchall_inventoryitemunit(self.connection)
        self.units_by_id = {unit.unitid: unit for unit in self.units}
        self.units_by_name = {unit.name: unit for unit in self.units}
        self.default_unit = self.units[0]

    def init_items(self) -> None:
        """Initialize the `items` member."""
        if not self.connection:
            raise NoDatabaseConnectionError
        self.items = database.fetchall_inventoryitem(self.connection,
                                                     self.units_by_id)
        self.items_by_id = {item.itemid: item for item in self.items}

    def create_inventoryitem(self, name: str, unit_name: str, notes: str
                             ) -> None:
        if not self.connection:
            raise NoDatabaseConnectionError
        unit = self.units_by_name[unit_name]
        new_itemid = database.create_inventoryitem(self.connection, name,
                                                   unit.unitid, notes)
        new_item = InventoryItem(new_itemid, name, unit, notes)
        self.items.append(new_item)
        self.items_by_id[new_itemid] = new_item

    def update_inventoryitem(self, item: InventoryItem) -> None:
        """Update inventory item in database.

        The caller is expected to have updated the items member.
        """
        if not self.connection:
            raise NoDatabaseConnectionError
        database.update_inventoryitem(self.connection, item)

    def delete_inventoryitem(self, itemid: int) -> None:
        if not self.connection:
            raise NoDatabaseConnectionError
        database.delete_inventoryitem(self.connection, itemid)
        deleted_item = self.items_by_id[itemid]
        self.items.remove(deleted_item)
        del self.items_by_id[itemid]


class ManageItemsPage(ttk.Frame):
    """View and update items."""
    def __init__(self, parent, inventory_database: InventoryDatabase, **kwargs
                 ) -> None:
        super().__init__(parent, **kwargs)

        self.inventory_database = inventory_database

        self.setup_ui()
        self.setup_callbacks()
        self.init_update_item_widget()
        self.item_view.refresh(self.inventory_database.items)

    def setup_ui(self) -> None:
        """Set up the user interface."""
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=0)
        self.rowconfigure(2, weight=0)

        self.item_view = InventoryItemView(self)
        self.item_view.grid(column=0, row=0, sticky="nsew")

        self.delete_button = ttk.Button(self, text="Delete Item")
        self.delete_button.grid(column=0, row=1, sticky="e", pady=(5,0))

        self.update_item_frame = ttk.Labelframe(self,
                                                text="Create Or Update Item")
        self.update_item_frame.columnconfigure(0, weight=1)
        self.update_item_frame.rowconfigure(0, weight=1)
        self.update_item_frame.grid(column=0, row=2, sticky="ew", pady=(10,0))
        
        self.update_item_widget = CreateOrUpdateInventoryItemWidget(
            self.update_item_frame)
        self.update_item_widget.grid(column=0, row=0, sticky="ew", padx=10,
                                     pady=(5,10))

    def setup_callbacks(self) -> None:
        """Set up callbacks for events."""
        self.item_view.on_select = self.set_update_item_widget_to_current_item
        self.delete_button["command"] = self.delete_item
        self.update_item_widget.on_reset = self.reset_page
        self.update_item_widget.on_update = self.update_item
        self.update_item_widget.on_create = self.create_item

    def reset_page(self) -> None:
        """Reset the page to its initial state."""
        self.item_view.clear_selection()
        self.reset_update_item_widget()

    def reset_update_item_widget(self) -> None:
        """Reset the `CreateOrUpdateItemWidget`."""
        self.update_item_widget.clear()
        self.update_item_widget.unit = self.inventory_database.default_unit.name
        self.update_item_widget.update_button["state"] = "disable"
        self.update_item_widget.create_button["state"] = "disable"
        self.delete_button["state"] = "disable"

    def delete_item(self) -> None:
        """Delete an item from the database."""
        self.inventory_database.delete_inventoryitem(
            self.item_view.current_itemid)
        self.item_view.refresh(self.inventory_database.items)
        self.reset_update_item_widget()

    def create_item(self) -> None:
        """Add an item to the database."""
        name = self.update_item_widget.name.strip()
        if not name:
            return
        self.inventory_database.create_inventoryitem(
            self.update_item_widget.name, self.update_item_widget.unit,
            self.update_item_widget.notes)
        self.item_view.refresh(self.inventory_database.items)
        self.reset_update_item_widget()
        self.update_item_widget.name_input.focus_set()

    def update_item(self) -> None:
        """Update an item in the database."""
        items_by_id = self.inventory_database.items_by_id
        current_item = items_by_id[self.item_view.current_itemid]
        current_item.name = self.update_item_widget.name
        units_by_name = self.inventory_database.units_by_name
        updated_unit = units_by_name[self.update_item_widget.unit]
        current_item.unit = updated_unit
        current_item.notes = self.update_item_widget.notes
        self.inventory_database.update_inventoryitem(current_item)
        self.item_view.refresh(self.inventory_database.items)
        self.item_view.view.selection_set(current_item.itemid)

    def set_update_item_widget_to_current_item(self) -> None:
        """Set the update item fields to current item values."""
        if not self.item_view.current_itemid:
            return
        items_by_id = self.inventory_database.items_by_id
        current_item = items_by_id[self.item_view.current_itemid]
        self.update_item_widget.name = current_item.name
        self.update_item_widget.unit = current_item.unit.name
        self.update_item_widget.notes = current_item.notes
        self.update_item_widget.update_button["state"] = "enable"
        self.delete_button["state"] = "enable"

    def init_update_item_widget(self) -> None:
        """Initialize the `CreateOrUpdateItemWidget`."""
        sorted_units = sorted(self.inventory_database.units_by_name.keys())
        self.update_item_widget.unit_choices = sorted_units
        self.reset_update_item_widget()
        self.setup_enable_disable_create_button()

    def setup_enable_disable_create_button(self) -> None:
        """Enable create button when input is valid."""
        self.name_variable = tk.StringVar()
        self.update_item_widget.name_input["textvariable"] = self.name_variable
        def enable_disable_create_button(*_):
            name = self.update_item_widget.name.strip()
            state = "normal" if name else "disable"
            self.update_item_widget.create_button["state"] = state
        self.name_variable.trace_add("write", enable_disable_create_button)


class TransactionPage(ttk.Frame):
    def __init__(self, parent, inventory_database: InventoryDatabase,  **kwargs):
        super().__init__(parent, **kwargs)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=0)

        # Boxed Items

        self.boxed_items_frame = ttk.Labelframe(self, text="Boxed Items")
        self.boxed_items_frame.columnconfigure(0, weight=1)
        self.boxed_items_frame.rowconfigure(0, weight=1)
        self.boxed_items_frame.rowconfigure(1, weight=0)
        self.boxed_items_frame.grid(column=0, row=0, sticky="nsew")

        self.boxed_items_view = InventoryItemView(self.boxed_items_frame)
        self.boxed_items_view.grid(column=0, row=0, sticky="nsew", padx=10,
                                   pady=(5,0))
        
        self.unbox_button = ttk.Button(self.boxed_items_frame, text="Unbox")
        self.unbox_button.grid(column=0, row=1, sticky="e", padx=10,
                               pady=(5,10))

        # Unboxed Items

        self.unboxed_items_frame = ttk.Labelframe(self, text="Unboxed Items")
        self.unboxed_items_frame.columnconfigure(0, weight=1)
        self.unboxed_items_frame.rowconfigure(0, weight=1)
        self.unboxed_items_frame.rowconfigure(1, weight=0)
        self.unboxed_items_frame.grid(column=0, row=1, sticky="nsew",
                                      pady=(5,0))

        self.unboxed_items_view = InventoryItemView(self.unboxed_items_frame)
        self.unboxed_items_view.grid(column=0, row=0, sticky="nsew",
                                     padx=10, pady=(5,10))
        
        self.unboxed_items_buttons_frame = ttk.Frame(self.unboxed_items_frame)
        self.unboxed_items_buttons_frame.columnconfigure(0, weight=0)
        self.unboxed_items_buttons_frame.columnconfigure(1, weight=0)
        self.unboxed_items_buttons_frame.rowconfigure(0, weight=0)
        self.unboxed_items_buttons_frame.grid(column=0, row=1, sticky="e",
                                              padx=10, pady=(5,10))

        self.box_all_button = ttk.Button(self.unboxed_items_buttons_frame,
                                         text="Box All")
        self.box_all_button.grid(column=0, row=0, sticky="e")

        self.box_one_button = ttk.Button(self.unboxed_items_buttons_frame,
                                         text="Box One")
        self.box_one_button.grid(column=1, row=0, sticky="e", padx=(5,0))

        # Transaction Control

        self.transact_control_frame = ttk.Labelframe(
                self, text="Transaction Control")
        self.transact_control_frame.columnconfigure(0, weight=1)
        self.transact_control_frame.rowconfigure(0, weight=0)
        self.transact_control_frame.rowconfigure(1, weight=0)
        self.transact_control_frame.rowconfigure(2, weight=0)
        self.transact_control_frame.grid(column=0, row=2, sticky="ew",
                                         pady=(5,0))

        self.transact_id_label = ttk.Label(self.transact_control_frame,
                                           text="Transaction ID: ")
        self.transact_id_label.grid(column=0, row=0, sticky="ew")

        self.items_in_transact_label = ttk.Label(self.transact_control_frame,
                                           text="Items in Transaction: ")
        self.items_in_transact_label.grid(column=0, row=1, sticky="ew",
                                          pady=(5,0))

        self.new_transaction_button = ttk.Button(self.transact_control_frame,
                                         text="New Transaction")
        self.new_transaction_button.grid(column=0, row=2, sticky="e",
                                         padx=10, pady=(5,10))


class Application:
    """Main class to handle GUI."""
    def __init__(self) -> None:
        self.inventory_database = InventoryDatabase()
        self.setup_ui()

    def setup_ui(self) -> None:
        """Set up the user interface."""
        self.root = tk.Tk()
        self.root.title("Home Inventory")
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        style = ttk.Style()
        style.theme_use("alt")

        self.main_notebook = ttk.Notebook(self.root, padding="10 10 10 10")
        self.main_notebook.grid(column=0, row=0)

        self.item_page = ManageItemsPage(self.root, self.inventory_database,
                                         padding="10 10 10 10")
        self.item_page.grid(column=0, row=0, sticky="nsew")

        self.transact_page = TransactionPage(self.root, self.inventory_database,
                                             padding="10 10 10 10")
        self.transact_page.grid(column=0, row=0, sticky="nsew")

        self.main_notebook.add(self.transact_page, text="Transaction")
        self.main_notebook.add(self.item_page, text="Manage Items")

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
