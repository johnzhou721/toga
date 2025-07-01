from __future__ import annotations
import warnings
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from toga.widgets.base import Widget
warnings.filterwarnings('default', category=DeprecationWarning)


class TogaApplicator:
    """Apply styles to a Toga widget."""

    def __init__(self, widget: None=None):
        if widget is not None:
            warnings.warn(
                "Widget parameter is deprecated. Applicator will be given a reference to its widget when it is assigned as that widget's applicator."
                , DeprecationWarning, stacklevel=2)

    @property
    def widget(self) ->Widget:
        """The widget to which this applicator is assigned.

        Syntactic sugar over the node attribute set by Travertino.
        """
        return self.node

    def refresh(self) ->None:
        self.widget.refresh()

    def set_bounds(self) ->None:
        self.widget._impl.set_bounds(self.widget.layout.
            absolute_content_left, self.widget.layout.absolute_content_top,
            self.widget.layout.content_width, self.widget.layout.content_height
            )
        for child in self.widget.children:
            child.applicator.set_bounds()

    def set_text_align(self, alignment: str) ->None:
        self.widget._impl.set_text_align(alignment)

    def set_hidden(self, hidden: bool) ->None:
        self.widget._impl.set_hidden(hidden)
        for child in self.widget.children:
            child.applicator.set_hidden(hidden or child.style._hidden)

    def set_font(self, font: object) ->None:
        self.widget._impl.set_font(font)

    def set_color(self, color: object) ->None:
        self.widget._impl.set_color(color)

    def set_background_color(self, color: object) ->None:
        self.widget._impl.set_background_color(color)
