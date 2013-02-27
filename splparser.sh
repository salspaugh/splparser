#!/bin/bash

function splparse {
    search=\'$1\' # bash will have stripped the quotes
    python -c "from splparser import parse; parse($search).print_tree()"    
}
