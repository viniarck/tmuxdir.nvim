import pynvim as vim
from typing import List

from tmuxdir.rplugin import TmuxDirPlugin, TmuxFacadeBinException
from tmuxdir.util import echoerr, expanduser_raise_if_not_dir


@vim.plugin
class TmuxDirRPlugin:
    def __init__(self, vim: vim.Nvim) -> None:
        self._rplugin = TmuxDirPlugin(vim)

    @vim.function("TmuxdirCheck", sync=True)
    def check_tmux_bin(self, args: List) -> bool:
        try:
            return self._rplugin.tmux_dir._check_tmux_bin()
        except TmuxFacadeBinException as e:
            echoerr(str(e), self._rplugin.plugin_name)
            return False

    @vim.function("TmuxdirAdd", sync=True)
    def tmuxdir_add(self, args: List) -> List[str]:
        if len(args) != 1:
            echoerr(
                self._rplugin.vim,
                "TmuxdirAdd expects a single argument",
                self._rplugin.plugin_name,
            )
            return []
        try:
            root_dir = expanduser_raise_if_not_dir(args[0])
            return self._rplugin.tmux_dir.add(root_dir)
        except OSError as e:
            echoerr(self._rplugin.vim, str(e), self._rplugin.plugin_name)
            return []

    @vim.function("TmuxdirClearAdded", sync=True)
    def tmuxdir_clear_added(self, args: List) -> bool:
        if len(args) != 1:
            echoerr(
                self._rplugin.vim,
                "TmuxdirClearAdded expects a single argument",
                self._rplugin.plugin_name,
            )
            return False
        try:
            root_dir = expanduser_raise_if_not_dir(args[0])
            return self._rplugin.tmux_dir.clear_added_dir(root_dir)
        except OSError as e:
            echoerr(self._rplugin.vim, str(e), self._rplugin.plugin_name)
            return False

    @vim.function("TmuxdirListAdded", sync=True)
    def tmuxdir_list_added(self, args: List) -> List[str]:
        return self._rplugin.tmuxdir_list_added()

    @vim.function("TmuxdirClearAddedAll", sync=True)
    def tmuxdir_clear_added_dirs(self, args: List) -> bool:
        return self._rplugin.tmux_dir.clear_added_dirs()

    @vim.function("TmuxdirIgnore", sync=True)
    def tmuxdir_ignore(self, args: List) -> bool:
        if len(args) != 1:
            echoerr(
                self._rplugin.vim,
                "TmuxdirIgnore expects a single argument",
                self._rplugin.plugin_name,
            )
            return False
        try:
            root_dir = expanduser_raise_if_not_dir(args[0])
            return self._rplugin.tmux_dir.ignore(root_dir)
        except OSError as e:
            echoerr(self._rplugin.vim, str(e), self._rplugin.plugin_name)
            return False

    @vim.function("TmuxdirClearIgnored", sync=True)
    def tmuxdir_clear_ignored(self, args: List) -> bool:
        if len(args) != 1:
            echoerr(
                self._rplugin.vim,
                "TmuxdirClearIgnored expects a single argument",
                self._rplugin.plugin_name,
            )
            return False
        try:
            root_dir = expanduser_raise_if_not_dir(args[0])
            return self._rplugin.tmux_dir.clear_ignored_dir(root_dir)
        except OSError as e:
            echoerr(self._rplugin.vim, str(e), self._rplugin.plugin_name)
            return False

    @vim.function("TmuxdirListIgnored", sync=True)
    def tmuxdir_list_ignored(self, args: List) -> List[str]:
        return self._rplugin.tmuxdir_list_ignored()

    @vim.function("TmuxdirClearIgnoredAll", sync=True)
    def tmuxdir_clear_ignored_dirs(self, args: List) -> bool:
        return self._rplugin.tmux_dir.clear_ignored_dirs()
