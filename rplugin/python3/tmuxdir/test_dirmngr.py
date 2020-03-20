import os
from tmuxdir.dirmngr import ConfigHandler, DirMngr
import pytest


@pytest.fixture
def dirmngr() -> None:
    pass
    config_handler = ConfigHandler()

class TestDirManager:
    def test_first_save(self):
        data = {"dirs": {"/tmp": "/tmp"}, "ignored_dirs": {}}
        ConfigHandler.save(data)
        loaded = ConfigHandler.load()
        assert loaded == data

    def test_bookmark_dir(self):
        dirs = ConfigHandler.load()
        dir_mngr = DirMngr([], [".git"])

        new_folder = "/tmp"
        os.makedirs(new_folder, exist_ok=True)
        assert dir_mngr.bookmark(new_folder)
        assert dir_mngr.dirs.keys() == dirs[dir_mngr._DIRS_KEY].keys()

    def test_add_dir_list(self):
        marker = ".pit"
        dir_mngr = DirMngr([], [marker])

        new_folder = "/tmp"
        os.makedirs(os.path.join(new_folder, marker), exist_ok=True)
        assert dir_mngr.add(new_folder)
        assert new_folder in dir_mngr.list_dirs()

    def test_add_ignore(self):
        marker = ".git"
        dir_mngr = DirMngr([], [marker])
        new_folder = "/tmp"
        os.makedirs(os.path.join(new_folder, marker), exist_ok=True)
        assert dir_mngr.add(new_folder)
        assert dir_mngr.ignore(new_folder)
        assert dir_mngr.ignored_dirs[new_folder] == new_folder
        assert new_folder not in dir_mngr.list_dirs()

    def test_clear_ignored_dirs(self):
        dir_mngr = DirMngr([], [".git"])
        new_folder = "/tmp"
        assert dir_mngr.bookmark(new_folder)
        assert dir_mngr.ignore(new_folder)
        dir_mngr.clear_ignored_dirs()
        assert dir_mngr.ignored_dirs == {}
        assert ConfigHandler.load()[dir_mngr._IGNORED_DIRS_KEY] == {}

    def test_clear_bookmarked_dirs(self):
        dir_mngr = DirMngr([], [".git"])
        new_folder = "/tmp"
        assert dir_mngr.bookmark(new_folder)
        dir_mngr.clear_bookmarked_dirs()
        assert dir_mngr.dirs == {}
        assert ConfigHandler.load()[dir_mngr._DIRS_KEY] == {}
