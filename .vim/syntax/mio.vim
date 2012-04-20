" Vim Syntax File
" Language:     mIo
" Creator:      James Mills, prologic at shortcircuit dot net dot au
" Last Change:  21st April 2012

if version < 600
    syntax clear
elseif exists("b:current_syntax")
    finish
endif

syntax case match

" equivalent to io-mode-prototype-names in io-mode.el
syntax keyword xType List Lobby
syntax keyword xType Message Number Object
syntax keyword xType String
syntax keyword xType True False None

" equivalent to io-mode-message-names in io-mode.el
syntax keyword xKeyword and arg at str bool break
syntax keyword xKeyword call catch clone continue
syntax keyword xKeyword do else elif exit for
syntax keyword xKeyword get has if id int float
syntax keyword xKeyword list message
syntax keyword xKeyword method not or parent pass eval
syntax keyword xKeyword print raise 
syntax keyword xKeyword del return
syntax keyword xKeyword set 
syntax keyword xKeyword slots super system then 
syntax keyword xKeyword call try type while
syntax keyword xKeyword write

syntax region xOperator start=':' end='='
syntax region xOperator start='!' end='='
syntax region xOperator start='\.' end='\.'
syntax region xOperator start='\.' end='[^\.]'he=e-1
syntax region xOperator start='=' end='='
syntax region xOperator start='=' end=' 'he=e-1
syntax region xOperator start='[*>=+-]' end='[ 0-9]'he=e-1

syntax region xString start=/"/ skip=/\\./ end=/"/
syntax region xString start=/"""/ skip=/\\./ end=/"""/

syntax region xComment start='#' end='$' keepend
syntax region xComment start=/\/\*/ end=/\*\//
syntax region xComment start=/\/\// end=/$/ keepend

highlight link xType Type
highlight link xKeyword Keyword
highlight link xString String
highlight link xComment Comment
highlight link xOperator Operator
highlight Operator ctermfg=5

let b:current_syntax = "mio"
