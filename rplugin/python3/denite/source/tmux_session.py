import denite.util as util
from denite.source.base import Base
from tmuxdir.tmux_session_facade import TmuxSessionFacade, TmuxFacadeException


class Source(Base):
    def __init__(self, vim):
        super().__init__(vim)

        self.name = "tmux_session"
        self.kind = "tmux_session"
        self.vim = vim
        self.sort_by = "__created_time"
        self.sort_reversed = True
        try:
            self.tmuxf = TmuxSessionFacade()
        except TmuxFacadeException as e:
            util.error(self.vim, str(e))

    def on_init(self, context):
        pass

    def highlight(self):
        self.vim.command("highlight default link {} Special".format(self.syntax_name))
        self.vim.command("highlight default link deniteTmuxSession Comment")

    def define_syntax(self):
        super().define_syntax()
        self.vim.command(
            "syntax match deniteTmuxSession /(.\{-})/ "
            "containedin=" + self.syntax_name
        )

    def gather_candidates(self, context):
        candidates = []
        for session in self.tmuxf.sessions().values():
            word = "{:40s} ({})".format(session.name, session.created_time)
            candidates.append(
                {
                    "word": word,
                    "__session_name": session.name,
                    "__created_time": session.created_time,
                }
            )
        return sorted(
            candidates, key=lambda x: x[self.sort_by], reverse=self.sort_reversed
        )
