" === basic vim setting ===

" syntax highlight
syntax on

" change comment highlight
highlight Comment ctermfg=darkcyan

" Hightlight Column bound
set colorcolumn=100
highlight ColorColumn ctermbg=darkblue

" Highlight current line
set cursorline
highlight CursorLine cterm=NONE ctermbg=darkgrey

" Visual mode color
highlight Visual cterm=NONE ctermbg=lightgray ctermfg=black

" set tab size
set expandtab
set tabstop=4
set shiftwidth=4

" increase search
set incsearch

" search highlight
set hlsearch
highlight Search ctermfg=gray ctermbg=darkblue

" show line number
set number

" setting Leader
let mapleader = ","

" setting auto complete notation when in .java .xml .c .cpp
autocmd Filetype java,xml,c,cpp inoremap <buffer> " ""<ESC>i
autocmd Filetype java,c,cpp inoremap <buffer> {<CR> {<ESC>o}<ESC>O

" enable plugin
filetype on
filetype indent on
filetype plugin on

" enable log file syntax highlight
au BufNewFile,BufRead *.log set filetype=log

" Set popup menu color
highlight Pmenu ctermbg=yellow ctermfg=black
highlight PmenuSel ctermbg=lightyellow ctermfg=black

" === plugin setting ===

" # pathogen
call pathogen#infect()

" # NERDTree
" close vim if the only window left open is a NERDTree
autocmd bufenter * if (winnr("$") == 1 && exists("b:NERDTreeType") && b:NERDTreeType == "primary") | q | endif
" Highlight Directory
highlight Directory ctermfg=lightblue

" # NERDTreeTabs
" Auto tabes on start
let g:nerdtree_tabs_open_on_console_startup=1

" # ShowMarks
" Show which marks
let showmarks_include = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
" Ignore help, quickfix, non-modifiable buffers
let showmarks_ignore_type = "hqm"
" highlight
hi ShowMarksHLl ctermbg=Yellow ctermfg=Black
hi ShowMarksHLu ctermbg=Magenta ctermfg=Black

" # Java Autocomplete
autocmd Filetype java set omnifunc=javacomplete#Complete
autocmd Filetype java set completefunc=javacomplete#CompleteParamsInf
inoremap <buffer> <C-X><C-U> <C-X><C-U><C-P>
inoremap <buffer> <C-S-Space> <C-X><C-U><C-P>
autocmd Filetype java inoremap <buffer> <TAB> <C-X><C-O><C-P>

" # FuzzyFinder
" Open file on new tab on pressing ENTER
let g:fuf_keyOpenTabpage="<CR>"
let g:fuf_keyOpen="<C-l>"
" Map key file search to F2
nnoremap <silent> <F2> lbyw:FufCoverageFile <C-R>"<CR>

