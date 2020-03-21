#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from pynvim import Nvim


def confirm(vim: Nvim, msg: str) -> bool:
    """Confirm action."""
    option: int = vim.call("confirm", msg, "&Yes\n&No")
    return option == 1


def echomsg(vim: Nvim, msg: str, label: str = "") -> None:
    """Vim echomsg."""
    label_expr = ""
    if label:
        label_expr = "[{}]:".format(label)
    vim.command('echomsg "{}{}"'.format(label_expr, msg))


def echoerr(vim: Nvim, msg: str, label: str = "") -> None:
    """Vim echoerr."""
    vim.command("echohl ErrorMsg")
    label_expr = ""
    if label:
        label_expr = "[{}]: ".format(label)
    vim.command('echomsg "{}{}"'.format(label_expr, msg))
    vim.command("echohl None")


def expanduser_raise_if_not_dir(root_dir: str) -> str:
    """expanduser and raise OSError if it's not a dir."""
    input_dir = os.path.expanduser(root_dir)
    if not os.path.isdir(input_dir):
        raise OSError("'{}' isn't a directory.".format(input_dir))
    return input_dir
