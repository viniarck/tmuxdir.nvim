import denite.util as util
from denite.source.base import Base
from tmuxdir.tmuxdir_facade import TmuxDirFacade, TmuxDirFacadeException


class Source(Base):
    def __init__(self, vim):
        super().__init__(vim)

        self.name: str = "tmux_dir"
        self.kind: str = "tmux_dir"
        self.vim = vim
        self.sort_by: str = "word"
        self.sort_reversed: bool = True

    def highlight(self):
        self.vim.command("highlight default link {} Special".format(self.syntax_name))

    def define_syntax(self):
        super().define_syntax()

    def gather_candidates(self, context):

        try:
            self.tmuxf = TmuxDirFacade(
                base_dirs=self.vim.eval("TmuxdirBaseDirs()"),
                root_markers=self.vim.eval("TmuxdirRootMarkers()"),
            )
        except TmuxDirFacadeException as e:
            util.error(self.vim, str(e))

        candidates = []
        for dir_path in self.tmuxf.list_dirs():
            candidates.append({"word": dir_path})
        return sorted(
            candidates, key=lambda x: x[self.sort_by], reverse=self.sort_reversed
        )
