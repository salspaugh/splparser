#!/bin/bash

function splparse {
    search=\'$1\' # bash will have stripped the quotes
    python -c "from splparser.parser import parse; parse($search, pdebug=True).print_tree()"    
}

function spllex {
    arg=\'$1\'
    python -c "from splparser.lexer import tokenize; print tokenize($arg)"
}
