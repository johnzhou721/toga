import toga


def test_scaffold_instantiation_uses_dummy_backend(app):
    """A scaffold is created with a Dummy backend implementation."""
    widget = toga.Box()
    scaffold = toga.Scaffold(content=widget)

    assert scaffold.content is widget
    assert type(scaffold._impl).__name__ == "Scaffold"
    assert scaffold._impl.__class__.__module__.startswith("toga_dummy")
