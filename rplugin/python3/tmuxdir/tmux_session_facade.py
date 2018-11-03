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
        self._sessions: Dict[str, TmuxSession] = {}

    def is_attached(self) -> bool:
        """Check if the local client is attached to tmux."""

        if os.environ.get("TMUX"):
            return True
        return False

    def _sync_sessions(self) -> None:
        """Synchronize current tmux sessions in memory."""

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

        # update
        if list(self._sessions.keys()) != list(sessions.keys()):
            self._sessions = sessions

    def list_sessions(self) -> List[TmuxSession]:
        """List tmux sessions.

        _sync_sessions first since sessions can be created/killed by other
        processes.
        """

        self._sync_sessions()
        return self._sessions.values()

    def exists_session(self, session_name) -> bool:
        """Check if a session exists
        Always _sync_sessions first since sessions can be created/killed.
        """

        self._sync_sessions()
        if self._sessions.get(session_name):
            return True
        return False

    def create_session(
        self,
        session_name: str,
        vim_bin_path: str,
        start_directory: str,
        vim_args: str = "e .",
    ) -> None:
        """Create a detached tmux session with nvim/vim started
        Raises TmuxFacadeException if an err occurs."""

        _cmd = ["tmux", "new-session", "-d"]

        if start_directory:
            _cmd.extend(["-c", start_directory])

        _cmd.extend(["-s", session_name])

        _cmd.append(vim_bin_path)
        if vim_args:
            _cmd.extend(["-c", vim_args])

        self._run_cmd(_cmd)

    def switch_session(self, session_name: str) -> None:
        """Switch to a tmux session
        Raises TmuxFacadeException if an err occurs."""

        if not self.is_attached():
            raise TmuxFacadeException(
                "Please, make sure you have a tmux session attached before trying to switch."
            )
        self._run_cmd(["tmux", "switch-client", "-t", session_name])

    def switch_or_create(
        self, session_name: str, start_directory: str, vim_args: str = ""
    ) -> None:
        """Either switch or create a new tmux session
        Raises TmuxFacadeException if an err occurs."""

        if not self.exists_session(session_name):
            if not self.is_attached():
                self.create_session(
                    session_name=session_name,
                    detached=False,
                    start_directory=start_directory,
                    vim_args=vim_args,
                )
                return
            else:
                self.create_session(
                    session_name=session_name,
                    detached=True,
                    start_directory=start_directory,
                    vim_args=vim_args,
                )
        self.switch_or_attach(session_name=session_name)

    def kill_session(self, session_name: str) -> None:
        """Kill a tmux session
        Raises TmuxFacadeException if an err occurs."""

        self._run_cmd(["tmux", "kill-session", "-t", session_name])

    def _check_tmux_bin(self) -> None:
        """Check if tmux binary can be found in the $PATH
        Raises TmuxFacadeBinException if an err occurs."""

        try:
            self._run_cmd(["tmux", "-V"])
        except TmuxFacadeException as e:
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
