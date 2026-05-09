class Scaffold:
    def __init__(self, interface, on_set_content=None):
        self.interface = interface
        self._content = None
        self._on_set_content = on_set_content

    def set_content(self, value):
        self._content = value
        if self._on_set_content:
            self._on_set_content(value)
