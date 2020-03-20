#!/usr/bin/env python
# -*- coding: utf-8 -*-
import subprocess
import os
import time
from typing import List, Dict


class TmuxFacadeException(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message


class TmuxFacadeBinException(TmuxFacadeException):
    def __init__(self, message):
        super().__init__(message)


class TmuxSession(object):

    """TmuxSession abstraction."""

    def __init__(self, name, created_epoch, attached) -> None:
        self.name = name
        self.created_epoch = created_epoch
        self.created_time = time.strftime(
            "%Y-%m-%d %H:%M:%S", time.localtime(int(created_epoch))
        )
        self.attached = attached

    def __repr__(self):
        return "TmuxSession(name={}, created_time={}, attached={})".format(
            self.name, self.created_time, self.attached
        )


class TmuxSessionFacade(object):

    """Abstraction responsible for switching, listing and creating tmux
    sessions from nvim/vim.

    tmux attaching won't be supported since tmux sessions inside nvim/vim
    is not desirable, which means you should have a tmux instance running
    to use this class.
    """

    def __init__(self) -> None:
        self._check_tmux_bin()

    def sessions(self) -> Dict[str, TmuxSession]:
        """Get existing tmux sessions."""
        sessions: Dict[str, TmuxSession] = {}
        out = self._run_cmd(
            [
                "tmux",
                "list-sessions",
                "-F",
                "#{session_name} #{session_created} #{session_attached}",
            ]
        )
        for line in out.splitlines():
            words = line.strip().split()
            if len(words) != 3:
                raise TmuxFacadeException("Failed to parse tmux list-sessions")
            sessions[words[0]] = TmuxSession(words[0], words[1], words[2])
        return sessions

    def is_attached(self) -> bool:
        """Check if the local client is attached to tmux."""
        if os.environ.get("TMUX"):
            return True
        return False

    def create(
        self,
        session_name: str,
        vim_bin_path: str,
        start_directory: str,
        vim_args: str = "e .",
    ) -> None:
        """Create a detached tmux session with nvim/vim started
        Raises TmuxFacadeException if an err occurs."""

        _cmd = [
            "tmux",
            "new-session",
            "-d",
            "-c",
            start_directory,
            "-s",
            session_name,
            vim_bin_path,
        ]
        if vim_args:
            _cmd.extend(["-c", vim_args])
        self._run_cmd(_cmd)

    def switch(self, session_name: str) -> None:
        """Switch to a tmux session
        Raises TmuxFacadeException if an err occurs."""

        if not self.is_attached():
            raise TmuxFacadeException(
                "Please, make sure you have a tmux session attached before"
                " trying to switch."
            )
        self._run_cmd(["tmux", "switch-client", "-t", session_name])

    def kill(self, session_name: str) -> None:
        """Kill a tmux session
        Raises TmuxFacadeException if an err occurs."""

        self._run_cmd(["tmux", "kill-session", "-t", session_name])

    def _check_tmux_bin(self) -> bool:
        """Check if tmux binary can be found in the $PATH
        Raises TmuxFacadeBinException if an err occurs."""

        try:
            self._run_cmd(["tmux", "-V"])
            return True
        except TmuxFacadeException:
            raise TmuxFacadeBinException(
                "tmux not found in $PATH. Make sure tmux is installed."
            )

    def _run_cmd(self, cmds: List[str]):
        """Run tmux commands via subprocess.
        Raises TmuxFacadeException if an err occurs."""

        try:
            out, err = subprocess.Popen(
                cmds,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
            ).communicate()
            if err:
                raise TmuxFacadeException(err)
            return out
        except (OSError, FileNotFoundError) as e:
            raise TmuxFacadeException(str(e))
