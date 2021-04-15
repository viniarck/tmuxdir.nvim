func! TmuxdirRootMarkers()
  if exists('g:tmuxdir_root_markers')
    return eval('g:tmuxdir_root_markers')
  else
    return [".git"]
  endif
endfunc

func! TmuxdirBaseDirs()
  if exists('g:tmuxdir_base_dirs')
    return eval('g:tmuxdir_base_dirs')
  else
    return []
  endif
endfunc

func! TmuxdirEagerMode()
  if exists('g:tmuxdir_eager_mode')
    return eval('g:tmuxdir_eager_mode')
  else
    return v:false
  endif
endfunc
