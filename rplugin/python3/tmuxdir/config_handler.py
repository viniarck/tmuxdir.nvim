#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import pickle
from typing import Dict


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
