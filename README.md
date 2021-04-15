![Python application](https://github.com/viniarck/tmuxdir.nvim/workflows/Python%20application/badge.svg?branch=master)

tmuxidir is a tmux session workspace plugin for nvim.

![tmuxdirlogo](https://lh3.googleusercontent.com/SYsERl-2msj8xkhf0m6oSJLorJESaE9yKKGNXZ9cfXYbYoJ9906bcCnGwB-xjgfAVWUtvL0KX7BujDlEmdD120nzhGiKHfaGqhbwR46fUsNIDvT07VALukCPq8G0nR2RlGzUT8K27sm1BwFZrwy3JMYRB3cKzvlNtWcQ4K-qZZxzyNP2rO-B0CyZPKSkP0zyfeotSguBTjFiMior_jc6tQjZD8jbsS9BWxiHsE_pkkDOhzlFWpC7PBPqXxP0zKn8CzGILu_mU8e_ODP4yC_YG-4kPm97XR-hnMbdW23EnKt7ygtvgg6oKsLSXggy5OjZP_zUb3y1cGr7us5so1sRq4WDZ7MKT1i4LUYhOwJ1Mbzb3QB1_OukRQaQUBG1aOvhTtzt2jUwPqgC-fYjyYkgp9h_Em0SUE5Uu665zG35jAjTq1193bgfxiGNty3Uo9vMNAWT9LjYPXsOsNLK6yXUlLKxBY2CJNv-7t0Lb6LDiFQ-LMYb8SoyByUDA9YR2mQIoO3zxf9tRvkhLh_2TNmab_R5Ut28OJnwoUl4pM3N1J3Ufe7eAyHo_haJc1bQPtpIqM-l7C1R-lqZpx_kjdzICgVchNZqBt06TLFyFoTgqhuiUNK2GGZ-IY6-XOyX6_88zmSkzdKEcLOlWwGR048jpTh-ktJLP1oi_1AhgPYxcnNHsYEDWM4juf83MTwZ240COu1t1h8Ga4VFioKjooRMFVQ2KkJt-8UJmUmxBcasaXenI84nUV4Frg=w500-h140-no)

## tmuxdir workflow

- Manage tmux sessions and projects from nvim.
- A project directory is identified with a root marker (folder or file) in a set of base directories (e.g.,`~/repos/`).
- Each project is mapped to a tmux session. You can open additional tmux sessions to the same project if you want as well.

### Features

- Denite source `tmux_session` for tmux sessions.
- Denite source `tmux_dir` for tmux project directories.
- Any folder can also be statically bookmarked as a project.
- Automatically discover new projects once a root marker is found.

## Screencast

- `:Denite tmux_session` and `:Denite tmux_dir`

![tmuxdir_final2_cropped.gif](https://s4.gifyu.com/images/tmuxdir_final2_cropped.gif)

## Installation

**Note:** tmuxdir requires [denite.nvim](https://github.com/Shougo/denite.nvim), pynvim, Neovim 0.3+ and Python3.6+

- If you use **dein**:

```viml
call dein#add('viniarck/tmuxdir.nvim')
call dein#add('Shougo/denite.nvim')
```

- If you use **vim-plug**:

```viml
Plug 'viniarck/tmuxdir.nvim', { 'do': ':UpdateRemotePlugins' }
Plug 'Shougo/denite.nvim'
```

## TLDR basic config


```viml
let g:tmuxdir_base_dirs = ['~/repos', '~/projects', '~/src'] " Set of base directories to look for your projects

let g:tmuxdir_root_markers = ['.git'] " root markers to identify projects
```

For more information, key bindings, and available functions, check [doc/tmuxdir.txt](doc/tmuxdir.txt) out.

## How to use

- Tmux sessions:

```
:Denite tmux_session
```

- Tmux project directories:

```
:Denite tmux_dir
```

## Docs / Release Notes

[tmuxdir.txt](./doc/tmuxdir.txt)
