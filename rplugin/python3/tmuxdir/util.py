#!/usr/bin/env python
# -*- coding: utf-8 -*-

from neovim import Nvim


def confirm(vim: Nvim, msg: str) -> bool:
    """Confirm action."""
    option: int = vim.call("confirm", msg, "&Yes\n&No")
    return option == 1
