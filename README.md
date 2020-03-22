![Python application](https://github.com/viniarck/tmuxdir.nvim/workflows/Python%20application/badge.svg?branch=master)

tmuxidir is a tmux session workspace plugin for nvim and vim.

## tmuxdir workflow

- Manage tmux sessions and projects from nvim/vim.
- A project directory is identified with a root marker (folder or file) in a set of base directories (e.g.,`~/repos/`).
- Each project is mapped to a tmux session.

### Features

- Denite source `tmux_session` for tmux sessions.
- Denite source `tmux_dir` for tmux project directories.
- Any folder can also be statically bookmarked as a project.
- Automatically discover new projects once a root marker is found.

## Screencast

- `:Denite tmux_session`

![tmux_sessions.gif](https://s5.gifyu.com/images/tmux_sessions.gif)

## Installation

**Note:** tmuxdir requires [denite.nvim](https://github.com/Shougo/denite.nvim), pynvim, Neovim 0.3+ or Vim8.1+ and Python3.6+

- If you use **dein**:

```viml
call dein#add('viniarck/tmuxdir.nvim')
if !has('nvim')
  call dein#add('roxma/nvim-yarp')
  call dein#add('roxma/vim-hug-neovim-rpc')
endif
call dein#add('Shougo/denite.nvim')
```

- If you use **vim-plug**:

```viml
if has('nvim')
  Plug 'viniarck/tmuxdir.nvim', { 'do': ':UpdateRemotePlugins' }
  Plug 'Shougo/denite.nvim'
else
  Plug 'viniarck/tmuxdir.nvim'
  Plug 'roxma/nvim-yarp'
  Plug 'roxma/vim-hug-neovim-rpc'
endif
  Plug 'Shougo/denite.nvim'
```

## TLDR basic config


```viml
let g:tmuxdir_base_dirs = ['~/repos', '~/projects', '~/src'] " Set of base directories to look for your projects

let g:tmuxdir_root_markers = ['.git'] " root markers to identify projects
```
- If you want to automatically discover new folders as you keep opening files/directories with nvim/vim:

```viml
augroup tmuxdir
    autocmd!
    autocmd VimEnter,DirChanged * silent! call TmuxdirAdd(getcwd())
augroup end
```

## How to use

- Tmux sessions:

```
:Denite tmux_session
```

- Tmux project directories:

```
:Denite tmux_dir
```

