import toga
from toga_dummy.utils import assert_action_performed_with


class TestWindowScaffold:
    """Tests for window scaffold management."""

    def test_window_scaffold_initialization(self, app):
        """A window initializes with no scaffold."""
        window = toga.Window()

        assert window._scaffold is None
        assert window.content is None

    def test_scaffold_property_readonly(self, app):
        """The _scaffold property can be set (internal use only)."""
        window = toga.Window()

        # _scaffold should be assignable internally
        window._scaffold = "dummy"
        assert window._scaffold == "dummy"

    def test_widget_assignment_creates_scaffold(self, app):
        """Assigning a widget creates an internal scaffold wrapper."""
        window = toga.Window()
        widget = toga.Box()

        window.content = widget

        # Content should return the widget
        assert window.content is widget
        # Scaffold should exist and wrap the widget
        assert window._scaffold is not None
        assert isinstance(window._scaffold, toga.Scaffold)
        assert window._scaffold.content is widget

    def test_direct_scaffold_assignment(self, app):
        """Assigning a scaffold directly uses it as-is."""
        window = toga.Window()
        inner_widget = toga.Box()
        scaffold = toga.Scaffold(content=inner_widget)

        window.content = scaffold

        # Content should return the scaffold
        assert window.content is scaffold
        # Internal scaffold should be the same scaffold
        assert window._scaffold is scaffold
        assert window._scaffold.content is inner_widget

    def test_scaffold_assignment_replaces_widget_scaffold(self, app):
        """Assigning a scaffold replaces a previous widget's scaffold."""
        window = toga.Window()
        widget1 = toga.Box()
        widget2 = toga.Box()
        scaffold2 = toga.Scaffold(content=widget2)

        # First assign a widget
        window.content = widget1
        first_scaffold = window._scaffold
        assert window.content is widget1

        # Then assign a scaffold directly
        window.content = scaffold2
        assert window.content is scaffold2
        assert window._scaffold is scaffold2
        # The original wrapper scaffold should be replaced
        assert window._scaffold is not first_scaffold

    def test_backend_set_scaffold_called_for_widget_assignment(self, app):
        """The backend receives the scaffold implementation on widget assignment."""
        window = toga.Window()
        widget = toga.Box()
        original_set_scaffold = window._impl.set_scaffold

        called = []

        def spy(scaffold_impl):
            called.append(scaffold_impl)
            return original_set_scaffold(scaffold_impl)

        window._impl.set_scaffold = spy
        window.content = widget

        assert len(called) == 1
        assert called[0] is window._scaffold._impl

    def test_backend_set_scaffold_called_for_direct_scaffold_assignment(self, app):
        """The backend receives the exact scaffold impl on direct assignment."""
        window = toga.Window()
        widget = toga.Box()
        scaffold = toga.Scaffold(content=widget)
        original_set_scaffold = window._impl.set_scaffold

        called = []

        def spy(scaffold_impl):
            called.append(scaffold_impl)
            return original_set_scaffold(scaffold_impl)

        window._impl.set_scaffold = spy
        window.content = scaffold

        assert len(called) == 1
        assert called[0] is scaffold._impl

    def test_dummy_backend_logs_set_scaffold_on_widget_assignment(self, app):
        """The dummy backend logs the set_scaffold call on widget assignment."""
        window = toga.Window()
        widget = toga.Box()

        window.content = widget

        # Check that set_scaffold was logged with the correct scaffold
        assert_action_performed_with(
            window, "set_scaffold", scaffold=window._scaffold._impl
        )

    def test_dummy_backend_logs_set_scaffold_on_direct_assignment(self, app):
        """The dummy backend logs the set_scaffold call on direct assignment."""
        window = toga.Window()
        widget = toga.Box()
        scaffold = toga.Scaffold(content=widget)

        window.content = scaffold

        # Check that set_scaffold was logged with the correct scaffold
        assert_action_performed_with(window, "set_scaffold", scaffold=scaffold._impl)

    def test_content_reassignment_clears_old_content(self, app):
        """Reassigning window content clears the previous widget's window."""
        window = toga.Window()
        widget1 = toga.Box()
        widget2 = toga.Box()

        window.content = widget1
        assert widget1.window is window

        window.content = widget2
        assert widget1.window is None
        assert window.content is widget2
        assert window._scaffold is not None
        assert window._scaffold.content is widget2

    def test_content_reassignment_with_old_content_without_window_attr(self, app):
        """Old content without a window attribute is ignored during reassignment."""
        window = toga.Window()
        widget = toga.Box()

        window._content = object()
        window.content = widget

        assert window.content is widget
        assert window._scaffold is not None
        assert window._scaffold.content is widget

    def test_scaffold_app_and_window_properties(self, app):
        """A scaffold exposes its associated app and window."""
        scaffold = toga.Scaffold()
        assert scaffold.app is None
        assert scaffold.window is None
        assert scaffold.toolbar is None  # Toolbar not implemented yet

        scaffold.app = app
        scaffold.window = toga.Window()
        assert scaffold.app is app
        assert scaffold.window is not None

    def test_scaffold_refresh_with_no_content(self, app):
        """Refreshing an empty scaffold is a no-op."""
        scaffold = toga.Scaffold()
        scaffold.refresh()

    def test_dummy_backend_logs_scaffold_attached_on_widget_assignment(self, app):
        """The dummy backend logs scaffold attachment on widget assignment."""
        window = toga.Window()
        widget = toga.Box()

        window.content = widget

        # Check that scaffold_attached was logged with the correct content
        assert_action_performed_with(window, "scaffold_attached", content=widget)

    def test_dummy_backend_logs_scaffold_attached_on_direct_assignment(self, app):
        """The dummy backend logs scaffold attachment on direct scaffold assignment."""
        window = toga.Window()
        widget = toga.Box()
        scaffold = toga.Scaffold(content=widget)

        window.content = scaffold

        # Check that scaffold_attached was logged with the correct content
        assert_action_performed_with(window, "scaffold_attached", content=widget)
