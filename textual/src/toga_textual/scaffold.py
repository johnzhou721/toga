from textual.containers import Container

from .utils import LoggedObject


class Scaffold(LoggedObject):
    def __init__(self, interface):
        super().__init__()
        self.interface = interface
        self._content = None
        self._toolbar = None

        # Create a container for toolbar and content
        self.native = Container()

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, value):
        if self._content:
            self.native.remove_children(self._content.native)
        self._content = value
        if value:
            self.native.mount(value.native)

    @property
    def toolbar(self):
        return self._toolbar

    @toolbar.setter
    def toolbar(self, value):
        if self._toolbar:
            self.native.remove_children(self._toolbar.native)
        self._toolbar = value
        if value:
            self.native.mount(value.native)  # Toolbar at top
