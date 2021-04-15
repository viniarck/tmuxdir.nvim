import os
from denite.kind.openable import Kind as Openable
from tmuxdir.tmuxdir_facade import TmuxDirFacade, TmuxDirFacadeException
from typing import List
import tmuxdir.util as util


class Kind(Openable):
    def __init__(self, vim) -> None:
        super().__init__(vim)

        self.name = "tmux_dir"
        self.default_action = "open"
        self.vim = vim
        self.has_nvim = self.vim.eval("has('nvim')")
        self.vim_bin_path = "vim"
        self.max_sessions = 10
        if self.has_nvim:
            self.vim_bin_path = "nvim"
        try:
            self.root_markers: List[str] = self.vim.eval("TmuxdirRootMarkers()")
            self.base_dirs: List[str] = self.vim.eval("TmuxdirBaseDirs()")
            self.tmux_dir = TmuxDirFacade(self.base_dirs, self.root_markers)
        except TmuxDirFacadeException as e:
            util.error(self.vim, str(e))

    def action_open(self, context: dict) -> None:
        """Open project dir in a tmux session. If the tmux dir session is already
        open, it switches to the session."""

        dir_path = context["targets"][0]["word"]
        session_name = self.tmux_dir.dir_to_session_name(dir_path=dir_path)

        if not self.tmux_dir.sessions().get(session_name):
            self.tmux_dir.create(
                session_name=session_name,
                vim_bin_path=self.vim_bin_path,
                start_directory=os.path.expanduser(dir_path),
            )
        try:
            self.tmux_dir.switch(session_name=session_name)
        except TmuxDirFacadeException as e:
            util.error(self.vim, str(e))

    def action_new(self, context: dict) -> None:
        """Open the project dir in a new tmux session."""

        dir_path = context["targets"][0]["word"]
        session_name = self.tmux_dir.dir_to_session_name(dir_path=dir_path)

        for i in range(self.max_sessions + 1):
            if i == 0:
                new_session_name = session_name
            else:
                new_session_name = f"{session_name}-{i}"

            if not self.tmux_dir.sessions().get(new_session_name):
                self.tmux_dir.create(
                    session_name=new_session_name,
                    vim_bin_path=self.vim_bin_path,
                    start_directory=os.path.expanduser(dir_path),
                )
                try:
                    self.tmux_dir.switch(session_name=new_session_name)
                except TmuxDirFacadeException as e:
                    util.error(self.vim, str(e))
                return

        util.error(
            self.vim,
            f"Maximum number of sessions {self.max_sessions} for this dir "
            f"{dir_path} has been reached.",
        )

    def action_delete(self, context: dict) -> None:
        """Ignore selected directory tmux session(s)."""
        if not util.confirm(
            self.vim,
            "Ignoring directory {}. Proceed?".format(
                [dirs["word"] for dirs in context["targets"]]
            ),
        ):
            return
        try:
            for item in context["targets"]:
                dir_path = item["word"]
                self.tmux_dir.ignore(input_dir=dir_path)
        except TmuxDirFacadeException as e:
            util.error(self.vim, str(e))
