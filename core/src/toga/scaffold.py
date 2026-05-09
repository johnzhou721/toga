from __future__ import annotations

from typing import TYPE_CHECKING, Any

from toga.platform import get_factory

if TYPE_CHECKING:
    from toga.widgets.base import Widget


class Scaffold:
    """Internal scaffold widget for managing window content and toolbar layout.

    This widget is used internally by Toga windows to provide a consistent
    interface for content management across different backends. It serves as
    an abstraction layer between the window's content assignment and the
    backend-specific layout and toolbar coordination.

    Applications should not create Scaffold instances directly. Instead,
    assign widgets or Scaffold instances to window.content, and Toga will
    manage the scaffold creation and assignment internally.
    """

    def __init__(
        self,
        content: Widget | None = None,
        **kwargs: Any,
    ):
        """Create a new scaffold.

        :param content: The content widget to be managed by this scaffold.
        """
        self._content = content
        self._toolbar = None  # Placeholder for future toolbar support
        self._app = None
        self._window = None
        self._impl = get_factory().Scaffold(interface=self)

    @property
    def content(self) -> Widget | None:
        """The content widget managed by this scaffold.

        :returns: The content widget, or None if no content has been set.
        """
        return self._content

    @property
    def toolbar(self):
        """The toolbar managed by this scaffold.

        :returns: The toolbar, or None if no toolbar has been set.
        """
        return self._toolbar

    @property
    def app(self):
        """The app that this scaffold is associated with."""
        return self._app

    @app.setter
    def app(self, app):
        self._app = app

    @property
    def window(self):
        """The window that this scaffold is associated with."""
        return self._window

    @window.setter
    def window(self, window):
        self._window = window

    def refresh(self):
        """Refresh the scaffold and its content."""
        if self._content:
            self._content.refresh()
