#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import Dict, List
from tmuxdir.tmux_session_facade import TmuxSessionFacade, TmuxFacadeException
from tmuxdir.dirmngr import DirMngr, ProjectDir
import os


class TmuxDirFacadeException(TmuxFacadeException):

    """TmuxDirFacadeException. """

    def __init__(self, message):
        """Constructor of TmuxDirFacadeException."""
        super().__init__(message)


class TmuxDirFacade(TmuxSessionFacade, DirMngr):

    """TmuxDirFacade Singleton."""

    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = object.__new__(TmuxDirFacade)
        return cls._instance

    def __init__(
        self, base_dirs: List[str], root_markers: List[str] = [".git"], eager_mode=False
    ) -> None:
        """Constructor of TmuxDirFacade."""
        TmuxSessionFacade.__init__(self)
        DirMngr.__init__(
            self, base_dirs=base_dirs, root_markers=root_markers, eager_mode=eager_mode
        )

    def dir_to_session_name(self, dir_path: str) -> str:
        """Convert a directory name to tmux session name."""

        def replace_dots(input_str: str, replace_with: str = "-"):
            """Replace dots since it's not allowed on tmux session names."""
            return input_str.replace(".", replace_with)
        return replace_dots(input_str=dir_path)
