from rubicon.objc import NSPoint, NSRect, NSSize
from travertino.size import at_least

from toga_cocoa.colors import native_color
from toga_cocoa.libs import NSTextAlignment, NSTextField

from .base import Widget


class Label(Widget):
    def create(self):
        self.native = NSTextField.alloc().init()

        self.native.drawsBackground = False
        self.native.editable = False
        self.native.bezeled = False

        # Add the layout constraints
        self.add_constraints()

    def set_text_align(self, value):
        self.native.alignment = NSTextAlignment(value)

    def set_color(self, value):
        self.native.textColor = native_color(value)

    def set_font(self, font):
        self.native.font = font._impl.native

    def get_text(self):
        return str(self.native.stringValue)

    def set_text(self, value):
        self.native.stringValue = value

    def rehint(self):
        # Width & height of a label is known and fixed.

        fictional_bounds = NSRect(NSPoint(0, 0), NSSize(1000000.0, 1000000.0))
        cell_size = self.native.cell.cellSizeForBounds(fictional_bounds)

        self.interface.intrinsic.width = at_least(cell_size.width)
        self.interface.intrinsic.height = cell_size.height
