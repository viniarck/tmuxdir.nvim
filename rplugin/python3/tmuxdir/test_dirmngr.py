import os
from tmuxdir.dirmngr import ConfigHandler, DirMngr
import pytest


@pytest.fixture
def dir_mngr() -> DirMngr:
    folder_name = "/tmp/tmuxdirtest/"
    os.makedirs(folder_name, exist_ok=True)
    cfg_handler = ConfigHandler(folder_name=folder_name)
    yield DirMngr([], [".git"], cfg_handler=cfg_handler)
    try:
        os.remove(str(cfg_handler._full_path))
    except FileNotFoundError:
        pass
    os.removedirs(folder_name)


@pytest.fixture
def cfg_handler() -> ConfigHandler:
    folder_name = "/tmp/tmuxdirtest/"
    os.makedirs(folder_name, exist_ok=True)
    config_handler = ConfigHandler(folder_name=folder_name)
    yield config_handler
    try:
        os.remove(str(config_handler._full_path))
    except FileNotFoundError:
        pass
    os.removedirs(folder_name)


@pytest.fixture
def tmp_git_folder() -> str:
    folder_name = "/tmp/repo/.git"
    os.makedirs(folder_name, exist_ok=True)
    yield "/".join(folder_name.split("/")[:-1])
    os.removedirs(folder_name)


class TestDirManager:
    def test_first_save(self, cfg_handler: ConfigHandler):
        data = {"dirs": {"/tmp": "/tmp"}, "ignored_dirs": {}}
        cfg_handler.save(data)
        loaded = cfg_handler.load()
        assert loaded == data

    def test_add_dir(self, dir_mngr: DirMngr, tmp_git_folder: str):
        assert dir_mngr.add(tmp_git_folder)[0] == tmp_git_folder
        assert dir_mngr.add("/tmp/foo") == []
        assert tmp_git_folder in dir_mngr.dirs

    def test_add_dir_list(self, dir_mngr: DirMngr, tmp_git_folder: str):
        folder = "/tmp/pit/"
        assert dir_mngr.add(folder) == []

    def test_add_clear(self, dir_mngr: DirMngr, tmp_git_folder: str):
        assert dir_mngr.add(tmp_git_folder) == [tmp_git_folder]
        assert dir_mngr.clear_added_dir(tmp_git_folder)
        assert dir_mngr.list_dirs() == []
        assert not dir_mngr.clear_added_dir("/tmp/random/")
        assert tmp_git_folder not in dir_mngr.dirs

    def test_clear_added_dirs(self, dir_mngr: DirMngr, tmp_git_folder: str):
        assert dir_mngr.add(tmp_git_folder)[0] == tmp_git_folder
        assert dir_mngr.clear_added_dir(tmp_git_folder)
        assert dir_mngr.dirs == {}
        assert dir_mngr.cfg_handler.load()[dir_mngr._DIRS_KEY] == {}

    def test_add_ignore(self, dir_mngr: DirMngr, tmp_git_folder: str):
        assert dir_mngr.add(tmp_git_folder) == [tmp_git_folder]
        assert dir_mngr.ignore(tmp_git_folder)
        assert dir_mngr.add(tmp_git_folder) == []
        assert tmp_git_folder not in dir_mngr.list_dirs()

    def test_clear_ignored_dirs(self, dir_mngr: DirMngr, tmp_git_folder: str):
        assert dir_mngr.add(tmp_git_folder)[0] == tmp_git_folder
        assert dir_mngr.ignore(tmp_git_folder)
        assert dir_mngr.clear_ignored_dirs()
        assert dir_mngr.ignored_dirs == {}
        assert dir_mngr.cfg_handler.load()[dir_mngr._IGNORED_DIRS_KEY] == {}

    @pytest.mark.skipif(
        not os.path.isdir(os.path.expanduser("~/b/repos")),
        reason="~/b/repos doesn't exist",
    )
    def test_find_projects_v10_eager(self, benchmark, dir_mngr: DirMngr) -> None:
        benchmark(dir_mngr.find_projects, "~/b/repos", [".git"], 3, True)

    @pytest.mark.skipif(
        not os.path.isdir(os.path.expanduser("~/b/repos")),
        reason="~/b/repos doesn't exist",
    )
    def test_find_projects_v11_not_eager(self, benchmark, dir_mngr: DirMngr) -> None:
        benchmark(dir_mngr.find_projects, "~/b/repos", [".git"], 3, False)
