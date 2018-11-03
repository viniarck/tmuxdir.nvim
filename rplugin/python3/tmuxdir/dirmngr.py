#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import pickle
import pathlib
from typing import Dict, List


class ProjectDir(object):

    """ProjectDir."""

    def __init__(self, name: str, start_directory: str) -> None:
        """Constructor of ProjectDir."""

        self.name = name
        self.start_directory = start_directory


class DirMngr(object):

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
    def find_dirs(cls, base_dir: str, root_markers: List[str]):
        """Find directories with root makers given a base directory."""

        def _sanitize_dir(input_dir: str) -> str:
            """Sanitize input_dir."""
            if input_dir:
                if input_dir[-1] == os.path.sep:
                    return input_dir[:-1]

        dirs = []
        for marker in root_markers:
            # non recursively first.
            f_dirs = pathlib.Path(os.path.expanduser(base_dir)).glob("*" + marker)
            for fdir in f_dirs:
                dir_name = str(fdir).split(marker)[0]
                dir_name = _sanitize_dir(dir_name)
                dirs.append(dir_name)
            else:
                # glob recursively
                f_dirs = pathlib.Path(os.path.expanduser(base_dir)).glob(
                    "*" + os.path.sep + "*" + marker
                )
                for fdir in f_dirs:
                    dir_name = str(fdir).split(marker)[0]
                    dir_name = _sanitize_dir(dir_name)
                    dirs.append(dir_name)
        return dirs

    def _load_dirs(self) -> None:
        """Load persisted dirs."""
        dirs = self.cfg_handler.load()
        if dirs:
            if dirs.get(self._DIRS_KEY):
                self.dirs = dirs[self._DIRS_KEY]
            if dirs.get(self._IGNORED_DIRS_KEY):
                self.ignored_dirs = dirs[self._IGNORED_DIRS_KEY]

    def _save_dirs(self):
        """Save all dirs."""
        dirs = {self._DIRS_KEY: self.dirs, self._IGNORED_DIRS_KEY: self.ignored_dirs}
        self.cfg_handler.save(dirs=dirs)

    def add(self, input_dir: str) -> bool:
        """Add a directory.

        Return true if suceeded, false otherwise."""
        input_dir = os.path.expanduser(input_dir)
        if not os.path.isdir(input_dir):
            return False
        if self.dirs.get(input_dir):
            return True

        self.dirs[input_dir] = input_dir
        self._save_dirs()
        return True

    def ignore(self, input_dir: str) -> bool:
        """Ignore a directory.

        Return true if succeeded, false otherwise."""
        input_dir = os.path.expanduser(input_dir)
        if self.ignored_dirs.get(input_dir):
            return True
        self.ignored_dirs[input_dir] = input_dir
        self._save_dirs()
        return True

    def clear_ignore(self) -> bool:
        """No longer ignore files."""
        self.ignored_dirs = {}
        self._save_dirs()
        return True

    def clear_extra_dirs(self) -> bool:
        """Clear all extra added dirs."""
        self.dirs = {}
        self._save_dirs()
        return True

    def clear_all(self) -> None:
        """Clear both extra added dirs and ignored dirs."""
        self.clear_extra_dirs()
        self.clear_ignore()
        return True

    def _sanitize_dir(self, input_dir: str) -> str:
        """Sanitize input_dir."""
        if input_dir:
            if input_dir[-1] == os.path.sep:
                return input_dir[:-1]
        return input_dir

    def list_dirs(self) -> List[str]:
        """List non ignored directories based on root markers."""
        dirs = []
        base_dirs = []
        if self._base_dirs:
            base_dirs.extend(self._base_dirs)
        if self.dirs:
            base_dirs.extend(self.dirs.keys())
        for input_dir in base_dirs:
            walked_dirs = DirMngr.find_dirs(input_dir, self._root_markers)
            for walked_dir in walked_dirs:
                if not self.ignored_dirs.get(walked_dir):
                    dirs.append(walked_dir)
        return dirs


class ConfigHandler(object):

    """ConfigHandler responsible for configuration serialization."""

    _config_name = "dirs.pickle"
    _config_folder = os.path.expanduser("~/.config/tmuxdir")
    _config_path = os.path.join(_config_folder, _config_name)
    os.makedirs(_config_folder, exist_ok=True)

    @classmethod
    def load(cls):
        """Load persisted directories."""
        try:
            with open(cls._config_path, "rb") as handle:
                return pickle.load(handle)
        except FileNotFoundError:
            return {}

    @classmethod
    def save(cls, dirs: Dict[str, str]):
        """Serialize directories on file system."""
        with open(cls._config_path, "wb") as handle:
            pickle.dump(dirs, handle, protocol=pickle.HIGHEST_PROTOCOL)


def test_first_save():
    data = {"dirs": {"/tmp": "/tmp"}, "ignored_dirs": {}}
    ConfigHandler.save(data)
    loaded = ConfigHandler.load()
    assert loaded == data


def test_add_dir():
    dirs = ConfigHandler.load()
    dir_mngr = DirMngr([], [".git"])

    new_folder = "/tmp"
    dirs[dir_mngr._DIRS_KEY][new_folder] = new_folder
    # new_folder must exist
    assert dir_mngr.add(new_folder)
    assert dir_mngr.dirs.keys() == dirs[dir_mngr._DIRS_KEY].keys()


def test_add_dir_list():
    marker = ".git"
    dir_mngr = DirMngr([], [marker])

    new_folder = "/tmp"
    assert dir_mngr.add(new_folder)
    os.makedirs(os.path.join(new_folder, marker), exist_ok=True)
    assert new_folder in dir_mngr.list_dirs()


def test_add_ignore():
    dir_mngr = DirMngr([], [".git"])
    new_folder = "/tmp"
    assert dir_mngr.add(new_folder)
    assert dir_mngr.ignore(new_folder)
    assert dir_mngr.ignored_dirs[new_folder] == new_folder
    assert new_folder not in dir_mngr.list_dirs()


def test_clear_ignore():
    dir_mngr = DirMngr([], [".git"])
    new_folder = "/tmp"
    assert dir_mngr.add(new_folder)
    assert dir_mngr.ignore(new_folder)
    dir_mngr.clear_ignore()
    assert dir_mngr.ignored_dirs == {}
    assert ConfigHandler.load()[dir_mngr._IGNORED_DIRS_KEY] == {}


def test_clear_extra_dirs():
    dir_mngr = DirMngr([], [".git"])
    new_folder = "/tmp"
    assert dir_mngr.add(new_folder)
    dir_mngr.clear_extra_dirs()
    assert dir_mngr.dirs == {}
    assert ConfigHandler.load()[dir_mngr._DIRS_KEY] == {}
