from __future__ import annotations
import importlib
import os
import sys
from functools import cache
from importlib import metadata
from types import ModuleType


def entry_points(*, group):
    if sys.version_info < (3, 10):
        return metadata.entry_points()[group]
    else:
        return metadata.entry_points(group=group)


_TOGA_PLATFORMS = {'android': 'android', 'darwin': 'macOS', 'ios': 'iOS',
    'linux': 'linux', 'freebsd': 'freeBSD', 'tvos': 'tvOS', 'watchos':
    'watchOS', 'wearos': 'wearOS', 'emscripten': 'web', 'win32': 'windows'}


def get_current_platform() ->(str | None):
    if hasattr(sys, 'getandroidapilevel'):
        return 'android'
    elif sys.platform.startswith('freebsd'):
        return 'freeBSD'
    else:
        return _TOGA_PLATFORMS.get(sys.platform)


current_platform = get_current_platform()


def find_backends():
    return sorted(set(entry_points(group='toga.backends')))


@cache
def get_platform_factory() ->ModuleType:
    """Determine the current host platform and import the platform factory.

    If the ``TOGA_BACKEND`` environment variable is set, the factory will be loaded
    from that module.

    Raises :any:`RuntimeError` if an appropriate host platform cannot be identified.

    :returns: The factory for the host platform.
    """
    if (backend_value := os.environ.get('TOGA_BACKEND')):
        try:
            factory = importlib.import_module(f'{backend_value}.factory')
        except ModuleNotFoundError as exc:
            toga_backends_values = ', '.join([f'{backend.value!r}' for
                backend in find_backends()])
            raise RuntimeError(
                f'The backend specified by TOGA_BACKEND ({backend_value!r}) could not be loaded ({exc}). It should be one of: {toga_backends_values}.'
                ) from exc
        else:
            pass
    else:
        toga_backends = find_backends()
        if len(toga_backends) == 0:
            raise RuntimeError('No Toga backend could be loaded.')
        elif len(toga_backends) == 1:
            backend = toga_backends[0]
        else:
            matching_backends = [backend for backend in toga_backends if 
                backend.name == current_platform]
            if len(matching_backends) == 0:
                toga_backends_string = ', '.join([
                    f'{backend.value!r} ({backend.name})' for backend in
                    toga_backends])
                raise RuntimeError(
                    f'Multiple Toga backends are installed ({toga_backends_string}), but none of them match your current platform ({current_platform!r}). Install a backend for your current platform, or use TOGA_BACKEND to specify a backend.'
                    )
            if len(matching_backends) > 1:
                toga_backends_string = ', '.join([
                    f'{backend.value!r} ({backend.name})' for backend in
                    matching_backends])
                raise RuntimeError(
                    f"Multiple candidate toga backends found: ({toga_backends_string}). Uninstall the backends you don't require, or use TOGA_BACKEND to specify a backend."
                    )
            backend = matching_backends[0]
        factory = importlib.import_module(f'{backend.value}.factory')
    return factory
