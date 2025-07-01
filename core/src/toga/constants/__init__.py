from enum import Enum, auto
from travertino.constants import *


class Direction(Enum):
    """The direction a given property should act."""
    HORIZONTAL = 0
    VERTICAL = 1


class Baseline(Enum):
    """The meaning of a Y coordinate when drawing text."""
    ALPHABETIC = auto()
    TOP = auto()
    MIDDLE = auto()
    BOTTOM = auto()


class FillRule(Enum):
    """The rule to use when filling paths."""
    EVENODD = 0
    NONZERO = 1


class FlashMode(Enum):
    """The flash mode to use when capturing photos or videos."""
    AUTO = -1
    OFF = 0
    ON = 1

    def __str__(self) ->str:
        return self.name.title()


class WindowState(Enum):
    """The possible window states of an app.

    NOTE: Some platforms do not fully support all states; see the :any:`toga.Window`'s
    platform notes for details.
    """
    NORMAL = 0
    """The ``NORMAL`` state represents the default state of the window or app when it is
    not in any other specific window state."""
    MINIMIZED = 1
    """``MINIMIZED`` state is when the window isn't currently visible, although it will
    appear in any operating system's list of active windows.
    """
    MAXIMIZED = 2
    """The window is the largest size it can be on the screen with title bar and window
    chrome still visible.
    """
    FULLSCREEN = 3
    """``FULLSCREEN`` state is when the window title bar and window chrome remain
    hidden; But app menu and toolbars remain visible.
    """
    PRESENTATION = 4
    """``PRESENTATION`` state is when the window title bar, window chrome, app menu
    and toolbars all remain hidden.

    A good example is a slideshow app in presentation mode - the only visible content
    is the slide.
    """
