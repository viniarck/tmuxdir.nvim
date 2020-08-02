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

if has('nvim')
    finish
endif

let s:tmuxdir = yarp#py3('tmuxdir_wrap')

func! TmuxdirCheck()
    return s:tmuxdir.call('check_tmux_bin')
endfunc

func! TmuxdirAdd(v)
    return s:tmuxdir.call('tmuxdir_add', a:v)
endfunc

func! TmuxdirClearAdded(v)
    return s:tmuxdir.call('tmuxdir_clear_added', a:v)
endfunc

func! TmuxdirListAdded()
    return s:tmuxdir.call('tmuxdir_list_added')
endfunc

func! TmuxdirClearAddedAll()
    return s:tmuxdir.call('tmuxdir_clear_added_dirs')
endfunc

func! TmuxdirIgnore(v)
    return s:tmuxdir.call('tmuxdir_ignore', a:v)
endfunc

func! TmuxdirClearIgnored(v)
    return s:tmuxdir.call('tmuxdir_clear_ignored', a:v)
endfunc

func! TmuxdirListIgnored()
    return s:tmuxdir.call('tmuxdir_list_ignored')
endfunc

func! TmuxdirClearIgnoredAll()
    return s:tmuxdir.call('tmuxdir_clear_ignored_dirs')
endfunc
