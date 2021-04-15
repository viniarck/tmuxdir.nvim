import pynvim as nvim
from typing import List

from tmuxdir.rplugin import TmuxDirPlugin
from tmuxdir.tmux_session_facade import TmuxFacadeException
from tmuxdir.util import echoerr, expanduser_raise_if_not_dir


@nvim.plugin
class TmuxDirRPlugin:
    def __init__(self, nvim: nvim.Nvim) -> None:

        try:
            self._rplugin = TmuxDirPlugin(nvim)
        except TmuxFacadeException as e:
            echoerr(nvim, str(e), "tmuxdir")

    @nvim.function("TmuxdirCheck", sync=True)
    def check_tmux_bin(self, args: List) -> bool:
        try:
            return self._rplugin.tmux_dir._check_tmux_bin()
        except TmuxFacadeException as e:
            echoerr(self._rplugin.nvim, str(e), self._rplugin.plugin_name)
        except AttributeError:
            echoerr(
                nvim,
                "tmux not found in $PATH. Make sure tmux is installed.",
                "tmuxdir",
            )
        return False

    @nvim.function("TmuxdirAdd", sync=True)
    def tmuxdir_add(self, args: List) -> List[str]:
        if len(args) != 1:
            echoerr(
                self._rplugin.nvim,
                "TmuxdirAdd expects a single argument",
                self._rplugin.plugin_name,
            )
            return []
        try:
            root_dir = expanduser_raise_if_not_dir(args[0])
            return self._rplugin.tmux_dir.add(root_dir)
        except OSError as e:
            echoerr(self._rplugin.nvim, str(e), self._rplugin.plugin_name)
            return []

    @nvim.function("TmuxdirClearAdded", sync=True)
    def tmuxdir_clear_added(self, args: List) -> bool:
        if len(args) != 1:
            echoerr(
                self._rplugin.nvim,
                "TmuxdirClearAdded expects a single argument",
                self._rplugin.plugin_name,
            )
            return False
        try:
            root_dir = expanduser_raise_if_not_dir(args[0])
            return self._rplugin.tmux_dir.clear_added_dir(root_dir)
        except OSError as e:
            echoerr(self._rplugin.nvim, str(e), self._rplugin.plugin_name)
            return False

    @nvim.function("TmuxdirListAdded", sync=True)
    def tmuxdir_list_added(self, args: List) -> List[str]:
        return self._rplugin.tmuxdir_list_added()

    @nvim.function("TmuxdirClearAddedAll", sync=True)
    def tmuxdir_clear_added_dirs(self, args: List) -> bool:
        return self._rplugin.tmux_dir.clear_added_dirs()

    @nvim.function("TmuxdirIgnore", sync=True)
    def tmuxdir_ignore(self, args: List) -> bool:
        if len(args) != 1:
            echoerr(
                self._rplugin.nvim,
                "TmuxdirIgnore expects a single argument",
                self._rplugin.plugin_name,
            )
            return False
        try:
            root_dir = expanduser_raise_if_not_dir(args[0])
            return self._rplugin.tmux_dir.ignore(root_dir)
        except OSError as e:
            echoerr(self._rplugin.nvim, str(e), self._rplugin.plugin_name)
            return False

    @nvim.function("TmuxdirClearIgnored", sync=True)
    def tmuxdir_clear_ignored(self, args: List) -> bool:
        if len(args) != 1:
            echoerr(
                self._rplugin.nvim,
                "TmuxdirClearIgnored expects a single argument",
                self._rplugin.plugin_name,
            )
            return False
        try:
            root_dir = expanduser_raise_if_not_dir(args[0])
            return self._rplugin.tmux_dir.clear_ignored_dir(root_dir)
        except OSError as e:
            echoerr(self._rplugin.nvim, str(e), self._rplugin.plugin_name)
            return False

    @nvim.function("TmuxdirListIgnored", sync=True)
    def tmuxdir_list_ignored(self, args: List) -> List[str]:
        return self._rplugin.tmuxdir_list_ignored()

    @nvim.function("TmuxdirClearIgnoredAll", sync=True)
    def tmuxdir_clear_ignored_dirs(self, args: List) -> bool:
        return self._rplugin.tmux_dir.clear_ignored_dirs()
