if !has('python3')
  finish
endif

" s:dir will be used in python
let s:dir= fnamemodify(resolve(expand('<sfile>:p')), ':h')
let s:path = s:dir . '/codespell.py'

" Config variables
"Function: s:initVariable() function {{{2
"This function is used to initialise a given variable to a given value. The
"variable is only initialised if it does not exist prior
"
"Args:
"var: the name of the var to be initialised
"value: the value to initialise var to
"
"Returns:
"1 if the var is set, 0 otherwise
function! s:initVariable(var, value)
    if !exists(a:var)
        exec 'let ' . a:var . ' = ' . "'" . substitute(a:value, "'", "''", "g") . "'"
        return 1
    endif
    return 0
endfunction

call s:initVariable("g:CodespellShortWord", 4)

function! CodeSpell()
  call clearmatches()
  execute 'py3file ' . s:path
endfunction

command! Codespell call CodeSpell()
