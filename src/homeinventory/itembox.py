from .common import Item


class ItemBox:
    def __init__(self, name: str) -> None:
        self.name = name
        self._items: list[Item] = []

    def __len__(self) -> int:
        return len(self._items)
