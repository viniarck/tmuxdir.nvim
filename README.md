tmuxdir is a project workspace plugin for neovim, fully integrated.

## Workflow

- Manage tmux sessions and projects from neovim, fully integrated with a few key strokes.
- Each project is identified with a file or directory called root marker, for example, `.git`.
- Each project is mapped to a tmux session. Once you're working in a project, if you need to save the workspace (buffers/windows), just create a vim session.

## Features

- Denite source for tmux sessions.
- Denite source for tmux project directories.
- Automatically discover new projects once a root marker is found.
