#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pynvim as nvim

from tmuxdir.tmuxdir_facade import TmuxDirFacade, TmuxFacadeException
from tmuxdir.dirmngr import DirMngr
from tmuxdir.util import expanduser_raise_if_not_dir, echoerr
from typing import List


class TmuxDirPlugin(object):

    """TmuxDirPlugin."""

    def __init__(self, nvim: nvim.Nvim) -> None:
        """Constructor of TmuxDirPlugin."""
        self.nvim = nvim
        self.plugin_name = "tmuxdir"

        # nvim settings
        self.root_markers: List[str] = self.nvim.eval("TmuxdirRootMarkers()")
        self.base_dirs: List[str] = self.nvim.eval("TmuxdirBaseDirs()")
        self._eager_mode: bool = self.nvim.eval("TmuxdirEagerMode()")

        self.dir_mngr = DirMngr(
            base_dirs=self.base_dirs,
            root_markers=self.root_markers,
            eager_mode=self._eager_mode,
        )

        self.tmux_dir = TmuxDirFacade(self.base_dirs, self.root_markers)
        try:
            self.tmux_dir._check_tmux_bin()
        except TmuxFacadeException as e:
            echoerr(self.nvim, str(e), self.plugin_name)

    def tmuxdir_add(self, args: List) -> List[str]:
        root_dir = expanduser_raise_if_not_dir(args[0])
        return self.tmux_dir.add(root_dir)

    def tmuxdir_clear_added(self, args: List) -> bool:
        root_dir = expanduser_raise_if_not_dir(args[0])
        return self.tmux_dir.clear_added_dir(root_dir)

    def tmuxdir_list_added(self) -> List[str]:
        return list(self.tmux_dir.dirs.keys())

    def tmuxdir_clear_added_dirs(self) -> bool:
        return self.tmux_dir.clear_added_dirs()

    def tmuxdir_ignore(self, args: List) -> bool:
        root_dir = expanduser_raise_if_not_dir(args[0])
        return self.tmux_dir.ignore(root_dir)

    def tmuxdir_clear_ignored(self, args: List) -> bool:
        root_dir = expanduser_raise_if_not_dir(args[0])
        return self.tmux_dir.clear_ignored_dir(root_dir)

    def tmuxdir_list_ignored(self) -> List[str]:
        return list(self.tmux_dir.ignored_dirs.keys())

    def tmuxdir_clear_ignored_dirs(self, args: List) -> bool:
        return self.tmux_dir.clear_ignored_dirs()

    def check_tmux_bin(self) -> bool:
        return self.tmux_dir._check_tmux_bin()
