#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import pickle
import pathlib
from typing import Dict, List, Set


class ProjectDir:

    """ProjectDir."""

    def __init__(self, name: str, start_directory: str) -> None:
        """Constructor of ProjectDir."""

        self.name = name
        self.start_directory = start_directory


class DirMngrException(Exception):
    def __init__(self, msg: str) -> None:
        """Constructor of DirMngrException."""
        self.msg = msg
        super().__init__(msg)


class DirMngr:

    """Manage Directory entries."""

    def __init__(self, base_dirs: List[str], root_markers: List[str]) -> None:
        """Constructor of DirMngr."""
        self._base_dirs: List[str] = base_dirs
        self._root_markers: List[str] = root_markers
        self._session_dirs: Dict[str, ProjectDir] = {}

        self._IGNORED_DIRS_KEY = "ignored_dirs"
        self._DIRS_KEY = "dirs"

        self.dirs: Dict[str, str] = {}
        self.ignored_dirs: Dict[str, str] = {}
        self.cfg_handler = ConfigHandler()

        self._load_dirs()

    @classmethod
    def find_projects(
        cls, root_dir: str, root_markers: List[str], depth=3, eager=True
    ) -> List[str]:
        """Find project directories given a root_dir and the depth to go through,
        if it's not eager it's going to return early."""
        dirs: List[str] = []

        def _remove_path_sep(input_dir: str) -> str:
            """Remove path separator."""
            if input_dir[-1] == os.path.sep:
                return input_dir[:-1]
            return input_dir

        def _find_projects(
            dirs: List[str],
            root_dir: str,
            root_markers: List[str],
            depth=3,
            cur_depth=1,
        ) -> List[str]:
            """Recursively find projects."""
            for marker in root_markers:
                expr = "{}{}{}".format(
                    (cur_depth - 1) * "*{}".format(os.path.sep), "*", marker
                )
                for d in pathlib.Path(os.path.expanduser(root_dir)).glob(expr):
                    dirs.append(os.path.sep.join(str(d).split(os.path.sep)[:-1]))
            if cur_depth == depth:
                return dirs
            else:
                if dirs and not eager:
                    return dirs
                return _find_projects(
                    dirs, root_dir, root_markers, depth, cur_depth + 1
                )

        return _find_projects(dirs, _remove_path_sep(root_dir), root_markers, depth)

    def _load_dirs(self) -> None:
        """Load persisted dirs."""
        dirs = self.cfg_handler.load()
        if dirs:
            if dirs.get(self._DIRS_KEY):
                self.dirs = dirs[self._DIRS_KEY]
            if dirs.get(self._IGNORED_DIRS_KEY):
                self.ignored_dirs = dirs[self._IGNORED_DIRS_KEY]

    def _save_dirs(self) -> None:
        """Save all dirs."""
        dirs = {self._DIRS_KEY: self.dirs, self._IGNORED_DIRS_KEY: self.ignored_dirs}
        self.cfg_handler.save(dirs=dirs)

    def add(self, input_dir: str) -> List[str]:
        """Add a project directory idempotently."""

        return [
            self._add(directory)
            for directory in self.find_projects(input_dir, self._root_markers)
        ]

    def bookmark(self, input_dir: str) -> str:
        """Bookmark a directory idempotently."""
        return self._add(input_dir)

    def _add(self, input_dir: str) -> str:
        """Statically add a directory idempotently."""

        input_dir = os.path.expanduser(input_dir)
        if not os.path.isdir(input_dir):
            raise DirMngrException("'{}' isn't a directory.".format(input_dir))
        if self.dirs.get(input_dir):
            return input_dir

        self.dirs[input_dir] = input_dir
        self._save_dirs()
        return input_dir

    def ignore(self, input_dir: str) -> bool:
        """Ignore a directory.

        Return true if succeeded, false otherwise."""
        input_dir = os.path.expanduser(input_dir)
        if self.ignored_dirs.get(input_dir):
            return True
        self.ignored_dirs[input_dir] = input_dir
        self._save_dirs()
        return True

    def clear_ignored_dirs(self) -> bool:
        """Clear all ignored dirs."""
        self.ignored_dirs = {}
        self._save_dirs()
        return True

    def clear_bookmarked_dirs(self) -> bool:
        """Clear all bookmarked dirs."""
        self.dirs = {}
        self._save_dirs()
        return True

    def clear_all(self) -> bool:
        """Clear both bookmarked dirs and ignored dirs."""
        self.clear_bookmarked_dirs()
        self.clear_ignored_dirs()
        return True

    def list_dirs(self) -> List[str]:
        """Unique list non ignored directories based on root markers."""
        base_dirs = []
        if self._base_dirs:
            base_dirs.extend(self._base_dirs)
        if self.dirs:
            base_dirs.extend(self.dirs.keys())
        dirs: Set[str] = set()
        for input_dir in base_dirs:
            for walked_dir in DirMngr.find_projects(input_dir, self._root_markers):
                if not self.ignored_dirs.get(walked_dir):
                    dirs.add(walked_dir)
        return list(dirs)


class ConfigHandler:

    """ConfigHandler responsible for configuration serialization."""

    def __init__(
        self, file_name="dirs.pickle", folder_name="~/.config/tmuxdir"
    ) -> None:
        self._file_name = file_name
        self._default_folder = folder_name
        self._folder = os.path.expanduser(
            os.environ.get("TMUXDIR_CONFIG_FOLDER", self._default_folder)
        )
        self._full_path = os.path.join(self._folder, self._file_name)

    def load(self):
        """Load persisted directories."""
        try:
            os.makedirs(self._folder, exist_ok=True)
            with open(self._full_path, "rb") as handle:
                return pickle.load(handle)
        except FileNotFoundError:
            return {}

    def save(self, dirs: Dict[str, Dict[str, str]]):
        """Serialize directories on file system."""
        with open(self._full_path, "wb") as handle:
            pickle.dump(dirs, handle, protocol=pickle.HIGHEST_PROTOCOL)
