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
        self, base_dirs: List[str], root_markers: List[str] = [".git"]
    ) -> None:
        """Constructor of TmuxDirFacade."""
        TmuxSessionFacade.__init__(self)
        DirMngr.__init__(self, base_dirs=base_dirs, root_markers=root_markers)

    def dir_to_session_name(self, dir_path: str) -> str:
        """Convert a directory name to tmux session name."""
        dir_split = dir_path.split(os.path.sep)
        index = -1

        def projects_dict() -> Dict[str, ProjectDir]:
            projects: Dict[str, ProjectDir] = {}
            for dir_path in self.list_dirs():
                name = dir_path.split(os.path.sep)[-2]
                projects[name] = ProjectDir(name=name, start_directory=dir_path)
            return projects

        def replace_dots(input_str: str, replace_with: str = "-"):
            """Replace dots since it's not allowed on tmux session names."""
            return input_str.replace(".", replace_with)

        projects = projects_dict()
        # recursively find the first non conflicting-key backwards
        for i in range(index, len(dir_split) * index, index):
            key = os.path.sep.join(dir_split[i:])
            if key and not projects.get(key):
                return replace_dots(input_str=key)
        return replace_dots(input_str=dir_path)
