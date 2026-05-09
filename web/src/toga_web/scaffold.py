from .utils import LoggedObject


class Scaffold(LoggedObject):
    def __init__(self, interface):
        super().__init__()
        self.interface = interface
        self._content = None
        self._toolbar = None

        # Create a div container for toolbar and content
        self.native = self.create_native_container()

    def create_native_container(self):
        """Create the native DOM container element."""
        container = self.interface.factory.not_implemented(
            "Scaffold.create_native_container()"
        )
        return container

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, value):
        self._content = value
        # Update DOM structure

    @property
    def toolbar(self):
        return self._toolbar

    @toolbar.setter
    def toolbar(self, value):
        self._toolbar = value
        # Update DOM structure
