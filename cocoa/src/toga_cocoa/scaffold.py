from toga_cocoa.libs import NSViewController


class Scaffold:
    def __init__(self, interface):
        self.interface = interface
        self._content = None
        self._toolbar = None  # NSToolbar instance

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

    def create_view_controller(self):
        """Create and return the NSViewController for this scaffold."""
        view_controller = NSViewController.alloc().init()
        # Set up the view controller with content and toolbar
        if self._content:
            view_controller.view = self._content.native
        # Toolbar setup would be here
        return view_controller
