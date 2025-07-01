from __future__ import annotations
import sys
import warnings
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any
if TYPE_CHECKING:
    from travertino.colors import hsl, rgb
from travertino.constants import BOLD, BOTTOM, CENTER, COLUMN, CURSIVE, END, FANTASY, HIDDEN, ITALIC, JUSTIFY, LEFT, LTR, MONOSPACE, NONE, NORMAL, OBLIQUE, RIGHT, ROW, RTL, SANS_SERIF, SERIF, SMALL_CAPS, START, SYSTEM, TOP, TRANSPARENT, VISIBLE
from travertino.layout import BaseBox
from travertino.properties.aliased import Condition, aliased_property
from travertino.properties.shorthand import directional_property
from travertino.properties.validated import list_property, validated_property
from travertino.size import BaseIntrinsicSize
from travertino.style import BaseStyle
from toga.fonts import FONT_STYLES, FONT_VARIANTS, FONT_WEIGHTS, SYSTEM_DEFAULT_FONT_SIZE, SYSTEM_DEFAULT_FONTS, Font, UnknownFontError
warnings.filterwarnings('default', category=DeprecationWarning)
NOT_PROVIDED = object()
PACK = 'pack'


class _AlignmentCondition(Condition):

    def __init__(self, main_value, /, **properties):
        super().__init__(**properties)
        self.main_value = main_value

    def match(self, style, main_name=None):
        return super().match(style) and getattr(style, f'_{main_name}'
            ) == self.main_value


class _alignment_property(validated_property):

    def __set_name__(self, owner, name):
        self.name = 'alignment'
        owner._BASE_ALL_PROPERTIES[owner].add('alignment')
        self.other = 'align_items'
        self.derive = {_AlignmentCondition(CENTER): CENTER,
            _AlignmentCondition(START, direction=COLUMN, text_direction=LTR
            ): LEFT, _AlignmentCondition(START, direction=COLUMN,
            text_direction=RTL): RIGHT, _AlignmentCondition(START,
            direction=ROW): TOP, _AlignmentCondition(END, direction=COLUMN,
            text_direction=LTR): RIGHT, _AlignmentCondition(END, direction=
            COLUMN, text_direction=RTL): LEFT, _AlignmentCondition(END,
            direction=ROW): BOTTOM}
        owner.align_items = _alignment_property(START, CENTER, END)
        owner.align_items.name = 'align_items'
        owner.align_items.other = 'alignment'
        owner.align_items.derive = {_AlignmentCondition(result, **condition
            .properties): condition.main_value for condition, result in
            self.derive.items()}

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        self.warn_if_deprecated()
        if hasattr(obj, f'_{self.other}'):
            for condition, value in self.derive.items():
                if condition.match(obj, main_name=self.other):
                    return value
        return super().__get__(obj)

    def __set__(self, obj, value):
        if value is self:
            return
        self.warn_if_deprecated()
        try:
            delattr(obj, f'_{self.other}')
        except AttributeError:
            pass
        else:
            pass
        super().__set__(obj, value)

    def __delete__(self, obj):
        self.warn_if_deprecated()
        try:
            delattr(obj, f'_{self.other}')
        except AttributeError:
            pass
        else:
            pass
        super().__delete__(obj)

    def is_set_on(self, obj):
        self.warn_if_deprecated()
        return super().is_set_on(obj) or hasattr(obj, f'_{self.other}')

    def warn_if_deprecated(self):
        if self.name == 'alignment':
            warnings.warn(
                'Pack.alignment is deprecated. Use Pack.align_items instead.',
                DeprecationWarning, stacklevel=3)


if sys.version_info < (3, 10):
    _DATACLASS_KWARGS = {'init': False, 'repr': False}
else:
    _DATACLASS_KWARGS = {'kw_only': True, 'repr': False}


@dataclass(**_DATACLASS_KWARGS)
class Pack(BaseStyle):
    _doc_link = ':doc:`style properties </reference/style/pack>`'


    class Box(BaseBox):
        pass


    class IntrinsicSize(BaseIntrinsicSize):
        pass
    _depth = -1
    display: str = validated_property(PACK, NONE, initial=PACK)
    visibility: str = validated_property(VISIBLE, HIDDEN, initial=VISIBLE)
    direction: str = validated_property(ROW, COLUMN, initial=ROW)
    align_items: str | None = validated_property(START, CENTER, END)
    justify_content: str | None = validated_property(START, CENTER, END,
        initial=START)
    gap: int = validated_property(integer=True, initial=0)
    width: str | int = validated_property(NONE, integer=True, initial=NONE)
    height: str | int = validated_property(NONE, integer=True, initial=NONE)
    flex: float = validated_property(number=True, initial=0)
    margin: int | tuple[int] | tuple[int, int] | tuple[int, int, int] | tuple[
        int, int, int, int] = directional_property('margin{}')
    margin_top: int = validated_property(integer=True, initial=0)
    margin_right: int = validated_property(integer=True, initial=0)
    margin_bottom: int = validated_property(integer=True, initial=0)
    margin_left: int = validated_property(integer=True, initial=0)
    color: rgb | hsl | str | None = validated_property(color=True)
    background_color: rgb | hsl | str | None = validated_property(TRANSPARENT,
        color=True)
    text_align: str | None = validated_property(LEFT, RIGHT, CENTER, JUSTIFY)
    text_direction: str | None = validated_property(RTL, LTR, initial=LTR)
    font_family: str | list[str] = list_property(*SYSTEM_DEFAULT_FONTS,
        string=True, initial=[SYSTEM])
    font_style: str = validated_property(*FONT_STYLES, initial=NORMAL)
    font_variant: str = validated_property(*FONT_VARIANTS, initial=NORMAL)
    font_weight: str = validated_property(*FONT_WEIGHTS, initial=NORMAL)
    font_size: int = validated_property(integer=True, initial=
        SYSTEM_DEFAULT_FONT_SIZE)
    horizontal_align_content: str | None = aliased_property(source={
        Condition(direction=ROW): 'justify_content'})
    horizontal_align_items: str | None = aliased_property(source={Condition
        (direction=COLUMN): 'align_items'})
    vertical_align_content: str | None = aliased_property(source={Condition
        (direction=COLUMN): 'justify_content'})
    vertical_align_items: str | None = aliased_property(source={Condition(
        direction=ROW): 'align_items'})
    padding: int | tuple[int] | tuple[int, int] | tuple[int, int, int] | tuple[
        int, int, int, int] = aliased_property(source='margin', deprecated=True
        )
    padding_top: int = aliased_property(source='margin_top', deprecated=True)
    padding_right: int = aliased_property(source='margin_right', deprecated
        =True)
    padding_bottom: int = aliased_property(source='margin_bottom',
        deprecated=True)
    padding_left: int = aliased_property(source='margin_left', deprecated=True)
    alignment: str | None = _alignment_property(TOP, RIGHT, BOTTOM, LEFT,
        CENTER)

    @classmethod
    def _debug(cls, *args: str) ->None:
        print('    ' * cls._depth, *args)

    @property
    def _hidden(self) ->bool:
        """Does this style declaration define an object that should be hidden."""
        return self.visibility == HIDDEN

    def _apply(self, names: set) ->None:
        if 'text_align' in names:
            if (value := self.text_align) is None:
                if self.text_direction == RTL:
                    value = RIGHT
                else:
                    value = LEFT
            self._applicator.set_text_align(value)
        if 'text_direction' in names:
            if self.text_align is None:
                self._applicator.set_text_align(RIGHT if self.
                    text_direction == RTL else LEFT)
        if 'color' in names:
            self._applicator.set_color(self.color)
        if 'background_color' in names:
            self._applicator.set_background_color(self.background_color)
        if 'visibility' in names:
            value = self.visibility
            if value == VISIBLE:
                widget = self._applicator.widget
                while (widget := widget.parent):
                    if widget.style._hidden:
                        value = HIDDEN
                        break
            self._applicator.set_hidden(value == HIDDEN)
        if names & {'font_family', 'font_size', 'font_style',
            'font_variant', 'font_weight'}:
            font = None
            font_kwargs = {'size': self.font_size, 'style': self.font_style,
                'variant': self.font_variant, 'weight': self.font_weight}
            for family in self.font_family:
                try:
                    font = Font(family, **font_kwargs)
                    break
                except UnknownFontError:
                    pass
                else:
                    pass
            if font is None:
                font = Font(SYSTEM, **font_kwargs)
                print(
                    f'No valid font family in {self.font_family}; using system font as a fallback'
                    )
            self._applicator.set_font(font)
        if names - {'text_align', 'color', 'background_color', 'visibility'}:
            self._applicator.refresh()

    def layout(self, viewport: Any) ->None:
        self.__class__._depth = -1
        self._layout_node(alloc_width=viewport.width, alloc_height=viewport
            .height, use_all_height=True, use_all_width=True)
        node = self._applicator.node
        node.layout.content_top = self.margin_top
        node.layout.content_bottom = self.margin_bottom
        node.layout.content_left = self.margin_left
        node.layout.content_right = self.margin_right

    def _layout_node(self, alloc_width: int, alloc_height: int,
        use_all_width: bool, use_all_height: bool) ->None:
        self.__class__._depth += 1
        node = self._applicator.node
        if self.width != NONE:
            available_width = self.width
            min_width = self.width
        else:
            available_width = max(0, alloc_width - self.margin_left - self.
                margin_right)
            if node.intrinsic.width is not None:
                try:
                    min_width = node.intrinsic.width.value
                    available_width = max(available_width, min_width)
                except AttributeError:
                    available_width = node.intrinsic.width
                    min_width = node.intrinsic.width
                else:
                    pass
            else:
                min_width = 0
        if self.height != NONE:
            available_height = self.height
            min_height = self.height
        else:
            available_height = max(0, alloc_height - self.margin_top - self
                .margin_bottom)
            if node.intrinsic.height is not None:
                try:
                    min_height = node.intrinsic.height.value
                    available_height = max(available_height, min_height)
                except AttributeError:
                    available_height = node.intrinsic.height
                    min_height = node.intrinsic.height
                else:
                    pass
            else:
                min_height = 0
        if node.children:
            min_width, width, min_height, height = self._layout_children(
                available_width=available_width, available_height=
                available_height, use_all_width=use_all_width,
                use_all_height=use_all_height)
        else:
            width = available_width
            height = available_height
        if self.width != NONE:
            width = self.width
            min_width = width
        if self.height != NONE:
            height = self.height
            min_height = height
        node.layout.content_width = int(width)
        node.layout.content_height = int(height)
        node.layout.min_content_width = int(min_width)
        node.layout.min_content_height = int(min_height)
        self.__class__._depth -= 1

    def _layout_node_in_direction(self, direction: str, alloc_main: int,
        alloc_cross: int, use_all_main: bool, use_all_cross: bool) ->None:
        if direction == COLUMN:
            self._layout_node(alloc_height=alloc_main, alloc_width=
                alloc_cross, use_all_height=use_all_main, use_all_width=
                use_all_cross)
        else:
            self._layout_node(alloc_width=alloc_main, alloc_height=
                alloc_cross, use_all_width=use_all_main, use_all_height=
                use_all_cross)

    def _layout_children(self, available_width: int, available_height: int,
        use_all_width: bool, use_all_height: bool) ->tuple[int, int, int, int]:
        horizontal = (LEFT, RIGHT) if self.text_direction == LTR else (RIGHT,
            LEFT)
        if self.direction == COLUMN:
            available_main, available_cross = available_height, available_width
            use_all_main, use_all_cross = use_all_height, use_all_width
            main_name, cross_name = 'height', 'width'
            main_start, main_end = TOP, BOTTOM
            cross_start, cross_end = horizontal
        else:
            available_main, available_cross = available_width, available_height
            use_all_main, use_all_cross = use_all_width, use_all_height
            main_name, cross_name = 'width', 'height'
            main_start, main_end = horizontal
            cross_start, cross_end = TOP, BOTTOM
        node = self._applicator.node
        flex_total = 0
        min_flex = 0
        main = 0
        min_main = 0
        remaining_main = available_main
        for i, child in enumerate(node.children):
            if child.style[main_name] != NONE:
                child.style._layout_node_in_direction(direction=self.
                    direction, alloc_main=remaining_main, alloc_cross=
                    available_cross, use_all_main=False, use_all_cross=
                    child.style.direction == self.direction)
                child_content_main = getattr(child.layout,
                    f'content_{main_name}')
                min_child_content_main = getattr(child.layout,
                    f'content_{main_name}')
            elif getattr(child.intrinsic, main_name) is not None:
                if hasattr(getattr(child.intrinsic, main_name), 'value'):
                    if child.style.flex:
                        flex_total += child.style.flex
                        child_content_main = getattr(child.intrinsic, main_name
                            ).value
                        min_child_content_main = child_content_main
                        min_flex += child.style[f'margin_{main_start}'
                            ] + child_content_main + child.style[
                            f'margin_{main_end}']
                    else:
                        child.style._layout_node_in_direction(direction=
                            self.direction, alloc_main=0, alloc_cross=
                            available_cross, use_all_main=False,
                            use_all_cross=child.style.direction == self.
                            direction)
                        child_content_main = getattr(child.layout,
                            f'content_{main_name}')
                        min_child_content_main = child_content_main
                else:
                    child.style._layout_node_in_direction(direction=self.
                        direction, alloc_main=remaining_main, alloc_cross=
                        available_cross, use_all_main=False, use_all_cross=
                        child.style.direction == self.direction)
                    child_content_main = getattr(child.layout,
                        f'content_{main_name}')
                    min_child_content_main = child_content_main
            elif child.style.flex:
                flex_total += child.style.flex
                child_content_main = 0
                min_child_content_main = 0
            else:
                child.style._layout_node_in_direction(direction=self.
                    direction, alloc_main=remaining_main, alloc_cross=
                    available_cross, use_all_main=False, use_all_cross=
                    child.style.direction == self.direction)
                child_content_main = getattr(child.layout,
                    f'content_{main_name}')
                min_child_content_main = getattr(child.layout,
                    f'min_content_{main_name}')
            gap = 0 if i == 0 else self.gap
            child_main = child.style[f'margin_{main_start}'
                ] + child_content_main + child.style[f'margin_{main_end}']
            main += gap + child_main
            remaining_main -= gap + child_main
            min_child_main = child.style[f'margin_{main_start}'
                ] + min_child_content_main + child.style[f'margin_{main_end}']
            min_main += gap + min_child_main
        if flex_total > 0:
            quantum = (remaining_main + min_flex) / flex_total
            for child in node.children:
                child_intrinsic_main = getattr(child.intrinsic, main_name)
                if child.style.flex and child_intrinsic_main is not None:
                    try:
                        ideal_main = quantum * child.style.flex
                        if child_intrinsic_main.value > ideal_main:
                            flex_total -= child.style.flex
                            min_flex -= child.style[f'margin_{main_start}'
                                ] + child_intrinsic_main.value + child.style[
                                f'margin_{main_end}']
                    except AttributeError:
                        pass
                    else:
                        pass
            if flex_total > 0:
                quantum = (min_flex + remaining_main) / flex_total
            else:
                quantum = 0
        else:
            quantum = 0
        for child in node.children:
            if child.style[main_name] != NONE:
                pass
            elif child.style.flex:
                if getattr(child.intrinsic, main_name) is not None:
                    try:
                        child_alloc_main = child.style[f'margin_{main_start}'
                            ] + getattr(child.intrinsic, main_name
                            ).value + child.style[f'margin_{main_end}']
                        ideal_main = quantum * child.style.flex
                        if ideal_main > child_alloc_main:
                            child_alloc_main = ideal_main
                        child.style._layout_node_in_direction(direction=
                            self.direction, alloc_main=child_alloc_main,
                            alloc_cross=available_cross, use_all_main=True,
                            use_all_cross=child.style.direction == self.
                            direction)
                        main = main - getattr(child.intrinsic, main_name
                            ).value + getattr(child.layout,
                            f'content_{main_name}')
                        min_main = min_main - getattr(child.intrinsic,
                            main_name).value + getattr(child.layout,
                            f'min_content_{main_name}')
                    except AttributeError:
                        pass
                    else:
                        pass
                else:
                    if quantum:
                        child_alloc_main = quantum * child.style.flex
                    else:
                        child_alloc_main = child.style[f'margin_{main_start}'
                            ] + child.style[f'margin_{main_end}']
                    child.style._layout_node_in_direction(direction=self.
                        direction, alloc_main=child_alloc_main, alloc_cross
                        =available_cross, use_all_main=True, use_all_cross=
                        child.style.direction == self.direction)
                    main += getattr(child.layout, f'content_{main_name}')
                    min_main += getattr(child.layout,
                        f'min_content_{main_name}')
            else:
                pass
        if use_all_main or self[main_name] != NONE:
            extra = max(0, available_main - main)
            main += extra
        else:
            extra = 0
        if self.justify_content == END:
            offset = extra
        elif self.justify_content == CENTER:
            offset = extra / 2
        else:
            offset = 0
        cross = 0
        min_cross = 0
        for child in node.children:
            if main_start == RIGHT:
                offset += child.layout.content_width + child.style.margin_right
                child.layout.content_left = main - offset
                offset += child.style.margin_left
            else:
                offset += child.style[f'margin_{main_start}']
                setattr(child.layout, f'content_{main_start}', offset)
                offset += getattr(child.layout, f'content_{main_name}')
                offset += child.style[f'margin_{main_end}']
            offset += self.gap
            child_cross = getattr(child.layout, f'content_{cross_name}'
                ) + child.style[f'margin_{cross_start}'] + child.style[
                f'margin_{cross_end}']
            cross = max(cross, child_cross)
            min_child_cross = child.style[f'margin_{cross_start}'] + getattr(
                child.layout, f'min_content_{cross_name}') + child.style[
                f'margin_{cross_end}']
            min_cross = max(min_cross, min_child_cross)
        if use_all_cross:
            cross = max(cross, available_cross)
        effective_align_items = self.align_items
        if cross_start == RIGHT:
            effective_cross_start = LEFT
            effective_cross_end = RIGHT
            if self.align_items == START:
                effective_align_items = END
            elif self.align_items == END:
                effective_align_items = START
        else:
            effective_cross_start = cross_start
            effective_cross_end = cross_end
        for child in node.children:
            extra = cross - (getattr(child.layout, f'content_{cross_name}') +
                child.style[f'margin_{effective_cross_start}'] + child.
                style[f'margin_{effective_cross_end}'])
            if effective_align_items == END:
                cross_start_value = extra + child.style[f'margin_{cross_start}'
                    ]
            elif effective_align_items == CENTER:
                cross_start_value = int(extra / 2) + child.style[
                    f'margin_{cross_start}']
            else:
                cross_start_value = child.style[f'margin_{cross_start}']
            setattr(child.layout, f'content_{effective_cross_start}',
                cross_start_value)
        if self.direction == COLUMN:
            return min_cross, cross, min_main, main
        else:
            return min_main, main, min_cross, cross

    def __css__(self) ->str:
        css = []
        if self.display == NONE:
            css.append('display: none;')
        else:
            pass
        if self.visibility != VISIBLE:
            css.append(f'visibility: {self.visibility};')
        css.append(f'flex-direction: {self.direction.lower()};')
        if (self.width == NONE and self.direction == ROW or self.height ==
            NONE and self.direction == COLUMN):
            css.append(f'flex: {self.flex} 0 auto;')
        if self.width != NONE:
            css.append(f'width: {self.width}px;')
        if self.height != NONE:
            css.append(f'height: {self.height}px;')
        if self.align_items:
            css.append(f'align-items: {self.align_items};')
        if self.justify_content != START:
            css.append(f'justify-content: {self.justify_content};')
        if self.gap:
            css.append(f'gap: {self.gap}px;')
        if self.margin_top:
            css.append(f'margin-top: {self.margin_top}px;')
        if self.margin_bottom:
            css.append(f'margin-bottom: {self.margin_bottom}px;')
        if self.margin_left:
            css.append(f'margin-left: {self.margin_left}px;')
        if self.margin_right:
            css.append(f'margin-right: {self.margin_right}px;')
        if self.color:
            css.append(f'color: {self.color};')
        if self.background_color:
            css.append(f'background-color: {self.background_color};')
        if self.text_align:
            css.append(f'text-align: {self.text_align};')
        if self.text_direction != LTR:
            css.append(f'text-direction: {self.text_direction};')
        if self.font_family != [SYSTEM]:
            families = [(f'"{family}"' if ' ' in family else family) for
                family in self.font_family]
            css.append(f"font-family: {', '.join(families)};")
        if self.font_size != SYSTEM_DEFAULT_FONT_SIZE:
            css.append(f'font-size: {self.font_size}pt;')
        if self.font_weight != NORMAL:
            css.append(f'font-weight: {self.font_weight};')
        if self.font_style != NORMAL:
            css.append(f'font-style: {self.font_style};')
        if self.font_variant != NORMAL:
            css.append(f'font-variant: {self.font_variant};')
        return ' '.join(css)
