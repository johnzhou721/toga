# Scaffold

```{eval-rst}
.. autoclass:: toga.Scaffold
    :members:
    :undoc-members:
```

## Usage

The `Scaffold` class is used internally by Toga windows to manage content layout and provide a foundation for future toolbar support. Applications should not create `Scaffold` instances directly. Instead, assign widgets or `Scaffold` instances to `window.content`, and Toga will handle scaffold management automatically.

### Assigning content to windows

```python
import toga

app = toga.App("My App", "org.example.myapp")
window = toga.Window()

# Assign a widget - Toga creates an internal scaffold
widget = toga.Box()
window.content = widget

# The window now has an internal scaffold wrapping the widget
assert window._scaffold is not None
assert window._scaffold.content is widget
```

### Direct scaffold assignment

```python
# Create a scaffold explicitly
scaffold = toga.Scaffold(content=widget)
window.content = scaffold

# The scaffold is used directly
assert window._scaffold is scaffold
```

## Internal API

The `_scaffold` property provides access to the window's current scaffold instance. This is intended for internal use by Toga backends and advanced users who need direct scaffold manipulation.
