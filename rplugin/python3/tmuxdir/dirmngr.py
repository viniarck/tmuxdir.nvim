#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import pathlib
from typing import Dict, List, Set
from tmuxdir.config_handler import ConfigHandler


class ProjectDir:

    """ProjectDir."""

    def __init__(self, name: str, start_directory: str) -> None:
        """Constructor of ProjectDir."""

        self.name = name
        self.start_directory = start_directory


class DirMngr:

    """Manage Directory entries."""

    def __init__(
        self,
        base_dirs: List[str],
        root_markers: List[str],
        cfg_handler: ConfigHandler = None,
    ) -> None:
        """Constructor of DirMngr."""
        self._base_dirs: List[str] = base_dirs
        self._root_markers: List[str] = root_markers
        self._session_dirs: Dict[str, ProjectDir] = {}

        self._IGNORED_DIRS_KEY = "ignored_dirs"
        self._DIRS_KEY = "dirs"

        self.dirs: Dict[str, str] = {}
        self.ignored_dirs: Dict[str, str] = {}

        self.cfg_handler = cfg_handler if cfg_handler else ConfigHandler()

        self._load_dirs()

    def find_projects(
        self, root_dir: str, root_markers: List[str], depth=3, eager=True
    ) -> List[str]:
        """Find project directories given a root_dir and the depth to go through,
        if it's not eager it's going to return early."""

        if not os.path.isdir(root_dir):
            return []

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

        def _get_non_existing_dirs(dirs: Dict[str, str]) -> Dict[str, str]:
            return {k: k for k, _ in dirs.items() if not os.path.isdir(k)}

        dirs = self.cfg_handler.load()
        if dirs:
            for key, attr in zip(
                (self._DIRS_KEY, self._IGNORED_DIRS_KEY,),
                ("dirs", "ignored_dirs"),
            ):
                if dirs.get(key):
                    loaded_dirs = dirs[key]
                    non_existing_loaded_dirs = _get_non_existing_dirs(loaded_dirs)
                    load_dict = {
                        k: v
                        for k, v in loaded_dirs.items()
                        if k not in non_existing_loaded_dirs
                    }
                    setattr(self, attr, load_dict)
            self._save_dirs()

    def _save_dirs(self) -> None:
        """Save all dirs."""
        dirs = {
            self._DIRS_KEY: self.dirs,
            self._IGNORED_DIRS_KEY: self.ignored_dirs,
        }
        self.cfg_handler.save(dirs=dirs)

    def add(self, input_dir: str) -> List[str]:
        """Add a project directory idempotently."""

        if input_dir in self.ignored_dirs:
            return []

        return [
            self._add(directory)
            for directory in self.find_projects(input_dir, self._root_markers)
        ]

    def _add(self, input_dir: str) -> str:
        """Statically add a directory idempotently."""

        if self.dirs.get(input_dir):
            return input_dir

        self.dirs[input_dir] = input_dir
        self._save_dirs()
        return input_dir

    def clear_added_dir(self, input_dir: str) -> bool:
        """Clear an added dir."""
        suceeded = bool(self.dirs.pop(input_dir, False))
        if suceeded:
            self._save_dirs()
        return suceeded

    def clear_added_dirs(self) -> bool:
        """Clear all added dirs."""
        self.dirs = {}
        self._save_dirs()
        return True

    def ignore(self, input_dir: str) -> bool:
        """Ignore a directory.

        Return true if succeeded, false otherwise."""
        if self.ignored_dirs.get(input_dir):
            return True
        self.ignored_dirs[input_dir] = input_dir
        self._save_dirs()
        return True

    def clear_ignored_dir(self, input_dir: str) -> bool:
        """Clear an ignored dir."""
        suceeded = bool(self.ignored_dirs.pop(input_dir, False))
        if suceeded:
            self._save_dirs()
        return suceeded

    def clear_ignored_dirs(self) -> bool:
        """Clear all ignored dirs."""
        self.ignored_dirs = {}
        self._save_dirs()
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
            for walked_dir in self.find_projects(input_dir, self._root_markers):
                if not self.ignored_dirs.get(walked_dir):
                    dirs.add(walked_dir)
        return list(dirs)
