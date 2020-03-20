import denite.util as util
from denite.source.base import Base
from tmuxdir.tmuxdir_facade import TmuxDirFacade, TmuxDirFacadeException
from typing import List


class Source(Base):
    def __init__(self, vim):
        super().__init__(vim)

        self.name: str = "tmux_dir"
        self.kind: str = "tmux_dir"
        self.vim = vim
        self.dirs: List[str] = []
        self.sort_by: str = "word"
        self.sort_reversed: bool = True

        # vim settings
        self.base_dirs: List[str] = []
        if int(self.vim.command_output("echo exists('g:tmuxdir_base_dirs')")):
            self.base_dirs = self.vim.eval("g:tmuxdir_base_dirs")
        self.root_markers: List[str] = [".git"]
        if int(self.vim.command_output("echo exists('g:tmuxdir_root_markers')")):
            self.root_markers = self.vim.eval("g:tmuxdir_root_markers")

        try:
            self.tmuxf = TmuxDirFacade(self.base_dirs, self.root_markers)
        except TmuxDirFacadeException as e:
            util.error(self.vim, str(e))

    def highlight(self):
        self.vim.command("highlight default link {} Special".format(self.syntax_name))

    def define_syntax(self):
        super().define_syntax()

    def gather_candidates(self, context):
        candidates = []
        for dir_path in self.tmuxf.list_dirs():
            candidates.append({"word": dir_path})
        return sorted(
            candidates, key=lambda x: x[self.sort_by], reverse=self.sort_reversed
        )
