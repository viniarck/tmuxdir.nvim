import denite.util
import tmuxdir.util as util
from denite.kind.openable import Kind as Openable
from tmuxdir.tmux_session_facade import TmuxSessionFacade, TmuxFacadeException


class Kind(Openable):
    def __init__(self, vim):
        super().__init__(vim)

        self.name = "tmux_session"
        self.default_action = "open"
        self.vim = vim
        self.tmuxf = TmuxSessionFacade()

    def action_open(self, context) -> None:
        """Switch to the first tmux selected session."""
        session_name = context["targets"][0]["word"]
        try:
            self.tmuxf.switch(session_name=session_name)
        except TmuxFacadeException as e:
            denite.util.error(self.vim, str(e))

    def action_delete(self, context) -> None:
        """Delete selected directory tmux session(s)."""
        if not util.confirm(
            self.vim,
            "Deleting tmux session(s) {}. Proceed?".format(
                [session["word"] for session in context["targets"]]
            ),
        ):
            return
        for item in context["targets"]:
            session_name = item["word"]
            try:
                self.tmuxf.kill(session_name=session_name)
            except TmuxFacadeException as e:
                denite.util.error(self.vim, str(e))
