from .utils import LoggedObject


class Scaffold(LoggedObject):
    def __init__(self, interface):
        super().__init__()
        self.interface = interface
        self._content = None
        self._toolbar = None

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, value):
        self._content = value

    @property
    def toolbar(self):
        return self._toolbar

    @toolbar.setter
    def toolbar(self, value):
        self._toolbar = value
