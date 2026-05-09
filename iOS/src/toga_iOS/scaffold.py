from toga_iOS.libs import (
    UINavigationController,
    UIViewController,
)

from .utils import LoggedObject


class Scaffold(LoggedObject):
    def __init__(self, interface):
        super().__init__()
        self.interface = interface
        self._content = None
        self._toolbar = None

        # Create navigation controller for toolbar management
        self.native = UINavigationController.alloc().init()

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, value):
        self._content = value
        if value:
            view_controller = UIViewController.alloc().init()
            view_controller.view = value.native
            self.native.viewControllers = [view_controller]

    @property
    def toolbar(self):
        return self._toolbar

    @toolbar.setter
    def toolbar(self, value):
        self._toolbar = value
        # Toolbar state maps to navigation bar visibility
