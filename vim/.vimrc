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

" There is comment formation in VIM
" But no useful to do following (Maybe it set earily)
"set formatoptions-=r
" Refer the following link to resolve it.
" http://disp.cc/b/11-3Trd

" setting Leader
let mapleader = ","

" setting auto complete notation when in .java .xml .c .cpp
"autocmd Filetype java,xml,c,cpp inoremap <buffer> " ""<ESC>i
"autocmd Filetype java,c,cpp inoremap <buffer> {<CR> {<ESC>o}<ESC>O
autocmd Filetype java,xml,c,cpp inoremap ' <c-r>=CompleteQuote("'")<CR>
autocmd Filetype java,xml,c,cpp inoremap " <c-r>=CompleteQuote('"')<CR>

" enable plugin
filetype on
filetype indent on
filetype plugin on

" enable log file syntax highlight
au BufNewFile,BufRead *.log set filetype=log

" Set popup menu color
highlight Pmenu ctermbg=yellow ctermfg=black
highlight PmenuSel ctermbg=lightyellow ctermfg=black

" Statusline
set laststatus=2
set statusline=%<%f\ %m%=\ %h%r\ %-19([%p%%]\ %3l,%02c%03V%)%y
highlight StatusLine ctermfg=blue ctermbg=white

" === plugin setting ===

" # pathogen
call pathogen#infect()

" # NERDTree
" close vim if the only window left open is a NERDTree
autocmd bufenter * if (winnr("$") == 1 && exists("b:NERDTreeType") && b:NERDTreeType == "primary") | q | endif
" Highlight Directory
highlight Directory ctermfg=lightblue
" Set default width of file explorer window
let g:NERDTreeWinSize=40

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

" === Define function ===

" # auto-complete Quotation

function! CompleteQuote(quote)
    let ql = len(split(getline('.'), a:quote, 1))-1
    let slen = len(split(strpart(getline("."), 0, col(".")-1), a:quote, 1))-1
    let elen = len(split(strpart(getline("."), col(".")-1), a:quote, 1))-1
    let isBefreQuote = getline('.')[col('.') - 1] == a:quote

    if (ql%2)==1
        " a:quote length is odd.
        return a:quote
    elseif ((slen%2)==1 && (elen%2)==1 && !isBefreQuote) || ((slen%2)==0 && (elen%2)==0)
        return a:quote . a:quote . "\<Left>"
    elseif isBefreQuote
        return "\<Right>"
    else
        return a:quote . a:quote . "\<Left>"
    endif
endfunction

