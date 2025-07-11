from __future__ import annotations

from warnings import filterwarnings, warn

# Make sure deprecation warnings are shown by default
filterwarnings("default", category=DeprecationWarning)


class Condition:
    def __init__(self, **properties):
        """A condition describing the values of one or more properties of a style.

        :param properties: Any number of name: value pairs
        """
        self.properties = properties

    def match(self, style):
        return all(style[name] == value for name, value in self.properties.items())

    def __str__(self):
        return "; ".join(
            f"{name} == {value}" for name, value in self.properties.items()
        )


class aliased_property:
    def __init__(self, source: str | dict, deprecated: bool = False):
        """Create a property that aliases an existing property.

        :param source: If this is a string, it is the name of the property to
            reference. Otherwise, it is a dictionary mapping conditions to the correct
            property name to use. If no condition is met, an AttributeError is raised.
        :deprecated: Is this property name deprecated?
        """
        self.source = source
        self.deprecated = deprecated

    def __set_name__(self, style_class, name):
        self.name = name
        style_class._BASE_ALL_PROPERTIES[style_class].add(name)

    def __get__(self, style, style_class=None):
        if style is None:
            return self

        return style[self.derive_name(style)]

    def __set__(self, style, value):
        if value is self:  # pragma: no-cover-if-lt-py310
            # This happens during autogenerated dataclass __init__ when no value is
            # supplied.
            return

        style[self.derive_name(style)] = value

    def __delete__(self, style):
        del style[self.derive_name(style)]

    def is_set_on(self, style):
        return self.derive_name(style) in style

    def derive_name(self, style):
        name = None

        if isinstance(self.source, str):
            name = self.source
        else:
            for condition, result in self.source.items():
                if condition.match(style):
                    name = result
                    break

        if name is None:
            conditions = " or ".join(f"({condition})" for condition in self.source)
            raise AttributeError(f"'{self.name}' is only supported when {conditions}")

        if self.deprecated:
            cls = type(style).__name__
            warn(
                f"{cls}.{self.name} is deprecated. Use {cls}.{name} instead.",
                DeprecationWarning,
                stacklevel=3,
            )

        return name
