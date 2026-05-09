from toga_gtk.libs import Gtk

from .utils import LoggedObject


class Scaffold(LoggedObject):
    def __init__(self, interface):
        super().__init__()
        self.interface = interface
        self._content = None
        self._toolbar = None

        # Create a vertical box to hold toolbar and content
        self.native = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, value):
        if self._content:
            self.native.remove(self._content.native)
        self._content = value
        if value:
            self.native.append(value.native)

    @property
    def toolbar(self):
        return self._toolbar

    @toolbar.setter
    def toolbar(self, value):
        if self._toolbar:
            self.native.remove(self._toolbar.native)
        self._toolbar = value
        if value:
            self.native.prepend(value.native)  # Toolbar at top
