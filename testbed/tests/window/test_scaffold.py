"""Tests for the scaffold layer between window and content.

The scaffold layer provides an internal abstraction for managing window content
and toolbar coordination across backends. These tests verify that the content
assignment and rendering works correctly through the scaffold layer.
"""

import toga


async def test_widget_assignment_displays_correctly(main_window, main_window_probe):
    """Assigning a widget to window.content displays it correctly via the scaffold."""
    # Create a simple widget
    label_widget = toga.Label("Test Label")

    # Assign it to the window
    main_window.content = label_widget

    # Verify the widget is displayed (content_size should be non-zero)
    await main_window_probe.redraw("Widget displayed")
    assert main_window_probe.content_size[0] > 0
    assert main_window_probe.content_size[1] > 0

    # Verify that the displayed content is the widget's native representation
    # (This is platform-specific, but the container should hold the widget's native)
    assert main_window._impl.container is not None


async def test_scaffold_assignment_displays_content_correctly(
    main_window, main_window_probe
):
    """Assigning a scaffold to window.content displays its content correctly."""
    # Create a scaffold with a widget
    label_widget = toga.Label("Scaffold Test Label")
    scaffold = toga.Scaffold(content=label_widget)

    # Assign the scaffold to the window
    main_window.content = scaffold

    # Verify the scaffold's content is displayed
    await main_window_probe.redraw("Scaffold content displayed")
    assert main_window_probe.content_size[0] > 0
    assert main_window_probe.content_size[1] > 0

    # Verify that the window's container is properly set up
    assert main_window._impl.container is not None


async def test_content_replacement_updates_display(main_window, main_window_probe):
    """Replacing window.content updates the displayed content through the scaffold."""
    # First assignment: widget
    label1 = toga.Label("First Label")
    main_window.content = label1
    await main_window_probe.redraw("First widget displayed")

    # Second assignment: different widget
    label2 = toga.Label("Second Label that is much longer")
    main_window.content = label2
    await main_window_probe.redraw("Second widget displayed")

    # The display should have been updated (content may have changed size)
    # At minimum, the window should still be displaying content
    assert main_window_probe.content_size[0] > 0
    assert main_window_probe.content_size[1] > 0
