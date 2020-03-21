import vim

from tmuxdir.rplugin import TmuxDirPlugin

_plugin = TmuxDirPlugin(vim)

# TODO catch exceptions.. and echoerr


def check_tmux_bin(*args):
    return _plugin.check_tmux_bin(args)


def tmuxdir_add(*args):
    return _plugin.tmuxdir_add(args)


def tmuxdir_clear_added(*args):
    return _plugin.tmuxdir_clear_added(args)


def tmuxdir_list_added(*args):
    return _plugin.tmuxdir_list_added()


def tmuxdir_clear_added_dirs(*args):
    return _plugin.tmuxdir_clear_added_dirs(args)


def tmuxdir_ignore(*args):
    return _plugin.tmuxdir_ignore(args)


def tmuxdir_clear_ignored(*args):
    return _plugin.tmuxdir_ignored(args)


def tmuxdir_list_ignored(*args):
    return _plugin.tmuxdir_list_ignored()


def tmuxdir_clear_ignored_dirs(*args):
    return _plugin.tmuxdir_ignored_dirs(args)
