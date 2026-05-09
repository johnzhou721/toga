class Scaffold:
    def __init__(self, interface):
        self.interface = interface
        self._content = None
        self._toolbar = None  # Placeholder for future toolbar support

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

    def refresh(self):
        if self._content:
            self._content.refresh()
