if !has('python')
    finish
endif

python import vim
python import sys
python sys.path.append(vim.eval('expand("<sfile>:h")'))
python import vimendeley

function! PrintAbstract()
python vimendeley.printAbstract()
endfunction

function! OpenPDF()
python vimendeley.openPDF()
endfunction

function! OpenWeb()
python vimendeley.openWeb()
endfunction

nmap <buffer>,t :call PrintAbstract() <cr>
nmap <buffer>,p :call OpenPDF() <cr>
nmap <buffer>,l :call OpenWeb() <cr>
