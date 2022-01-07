from operator import itemgetter

from wagtailstreamforms.conf import get_setting
from wagtailstreamforms.utils.apps import get_app_submodules

_hooks = {}


def register(hook_name, fn=None, order=0):
    """
    Register hook for ``hook_name``. Can be used as a decorator::
        @register('hook_name')
        def my_hook(...):
            pass
    or as a function call::
        def my_hook(...):
            pass
        register('hook_name', my_hook)
    """

    # Pretend to be a decorator if fn is not supplied
    if fn is None:

        def decorator(fn):
            register(hook_name, fn, order=order)
            return fn

        return decorator

    if hook_name not in _hooks:
        _hooks[hook_name] = []
    _hooks[hook_name].append((fn, order))


_searched_for_hooks = False


def search_for_hooks():
    global _searched_for_hooks
    if not _searched_for_hooks:
        list(get_app_submodules("wagtailstreamforms_hooks"))
        _searched_for_hooks = True


def get_hooks(hook_name):
    """Return the hooks function sorted by their order."""

    search_for_hooks()
    hooks = _hooks.get(hook_name, [])
    hooks = sorted(hooks, key=itemgetter(1))
    fncs = []
    builtin_hook_modules = ["wagtailstreamforms.wagtailstreamforms_hooks"]
    builtin_enabled = get_setting("ENABLE_BUILTIN_HOOKS")

    for fn, _ in hooks:
        # dont add the hooks if they have been disabled via the setting
        # this is so that they can be overridden
        if fn.__module__ in builtin_hook_modules and not builtin_enabled:
            continue
        fncs.append(fn)

    return fncs
