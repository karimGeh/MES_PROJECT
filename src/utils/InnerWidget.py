class InnerWidget:
    _index = 0

    def __init__(self, master, WidgetClass) -> None:
        self.innerWidget = WidgetClass(master)
        self.index = self._index
        InnerWidget._index += 1
