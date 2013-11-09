" Vim Syntax File
" Language:     mio
" Creator:      James Mills, prologic at shortcircuit dot net dot au
" Last Change:  21st April 2012

if version < 600
    syntax clear
elseif exists("b:current_syntax")
    finish
endif

syntax case match

" equivalent to io-mode-prototype-names in io-mode.el
syntax keyword xType File Root List Tuple
syntax keyword xType Dict Message Number Object
syntax keyword xType String Range System
syntax keyword xType True False None

" equivalent to io-mode-message-names in io-mode.el
syntax keyword xKeyword arg at str bool break
syntax keyword xKeyword call catch clone continue
syntax keyword xKeyword dict do foreach filter
syntax keyword xKeyword get has ifTrue ifFalse id hash type
syntax keyword xKeyword list map block method parent eval
syntax keyword xKeyword print println raise 
syntax keyword xKeyword del range return reduce yield
syntax keyword xKeyword sum set keys summary
syntax keyword xKeyword super try while write writeln

syntax keyword xOperator is or and not return

syntax region xString start=/"/ skip=/\\./ end=/"/
syntax region xString start=/"""/ skip=/\\./ end=/"""/

syntax region xComment start='#' end='$' keepend

highlight link xType Type
highlight link xKeyword Keyword
highlight link xString String
highlight link xComment Comment
highlight link xOperator Operator
highlight Operator ctermfg=5

let b:current_syntax = "mio"
