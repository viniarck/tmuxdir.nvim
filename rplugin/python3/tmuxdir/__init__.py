import neovim

from tmuxdir.tmux_session_facade import TmuxFacadeBinException
from tmuxdir.tmuxdir_facade import TmuxDirFacade
from tmuxdir.dirmngr import DirMngr
from typing import List


@neovim.plugin
class TmuxDirPlugin(object):

    """TmuxDirPlugin."""

    def __init__(self, nvim) -> None:
        """Constructor of TmuxDirPlugin."""
        self.nvim = nvim

        # vim settings
        self.root_markers: List[str] = [".git"]
        if int(self.nvim.command_output("echo exists('g:tmuxdir_root_markers')")):
            self.root_markers = self.nvim.eval("g:tmuxdir_root_markers")
        self.base_dirs: List[str] = []
        if int(self.nvim.command_output("echo exists('g:tmuxdir_base_dirs')")):
            self.base_dirs = self.nvim.eval("g:tmuxdir_base_dirs")
        self.dir_mngr = DirMngr(
            base_dirs=self.base_dirs, root_markers=self.root_markers
        )

        self.tmux_dir = TmuxDirFacade(self.base_dirs, self.root_markers)
        self.tmux_dir._check_tmux_bin()

    @neovim.function("TmuxdirAdd", sync=True)
    def tmuxdir_add(self, args: List) -> bool:
        if len(args) > 1:
            self.nvim.err_write("TmuxdirAdd expects a single argument")
            return False
        return self.tmux_dir.add(args[0])

    @neovim.function("TmuxdirIgnore", sync=True)
    def tmuxdir_ignore(self, args: List) -> bool:
        if len(args) > 1:
            self.nvim.err_write("TmuxdirIgnore expects a single argument")
            return False
        return self.tmux_dir.ignore(args[0])

    @neovim.function("TmuxdirClearIgnore", sync=True)
    def tmuxdir_clear_ignore(self, args: List) -> bool:
        return self.tmux_dir.clear_ignore()

    @neovim.function("TmuxdirClearExtraDirs", sync=True)
    def tmuxdir_clear_extra_dirs(self, args: List) -> bool:
        return self.tmux_dir.clear_extra_dirs()

    @neovim.function("TmuxdirClear", sync=True)
    def tmuxdir_clear(self, args: List) -> bool:
        return self.tmux_dir.clear_all()

    @neovim.function("TmuxdirCheck", sync=True)
    def check_tmux_bin(self, args: List) -> str:
        try:
            self.tmux_dir._check_tmux_bin()
            return True
        except TmuxFacadeBinException as e:
            self.nvim.err_write(e.message)
