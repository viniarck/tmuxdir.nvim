import vim

from tmuxdir.rplugin import TmuxDirPlugin, TmuxFacadeException
from tmuxdir.util import echoerr

try:
    _plugin = TmuxDirPlugin(vim)
except TmuxFacadeException as e:
    echoerr(vim, str(e), "tmuxdir")


def check_tmux_bin(*args):
    try:
        return _plugin.check_tmux_bin()
    except TmuxFacadeException as e:
        echoerr(_plugin.vim, str(e), _plugin.plugin_name)
    except (AttributeError, NameError):
        echoerr(
            vim,
            "tmux not found in $PATH. Make sure tmux is installed.",
            "tmuxdir",
        )


def tmuxdir_add(*args):
    try:
        return _plugin.tmuxdir_add(args)
    except OSError as e:
        echoerr(_plugin.vim, str(e), _plugin.plugin_name)


def tmuxdir_static_add(*args):
    try:
        return _plugin.tmuxdir_add_static(args)
    except OSError as e:
        echoerr(_plugin.vim, str(e), _plugin.plugin_name)


def tmuxdir_clear_added(*args):
    try:
        return _plugin.tmuxdir_clear_added(args)
    except OSError as e:
        echoerr(_plugin.vim, str(e), _plugin.plugin_name)


def tmuxdir_list_added(*args):
    return _plugin.tmuxdir_list_added()


def tmuxdir_clear_added_dirs(*args):
    return _plugin.tmuxdir_clear_added_dirs()


def tmuxdir_ignore(*args):
    try:
        return _plugin.tmuxdir_ignore(args)
    except OSError as e:
        echoerr(_plugin.vim, str(e), _plugin.plugin_name)


def tmuxdir_clear_ignored(*args):
    try:
        return _plugin.tmuxdir_clear_ignored(args)
    except OSError as e:
        echoerr(_plugin.vim, str(e), _plugin.plugin_name)


def tmuxdir_list_ignored(*args):
    return _plugin.tmuxdir_list_ignored()


def tmuxdir_clear_ignored_dirs(*args):
    return _plugin.tmuxdir_ignored_dirs(args)
