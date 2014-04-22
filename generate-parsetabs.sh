#!/bin/bash

function generate_parsetabs {
    for cmd in `cat ${SPLPARSER_HOME}/all_commands.txt`; do
        echo "Generating LALR parser tables for ${cmd}...\c"
        python -c "from splparser.parser import parse; parse('$cmd')" &> /dev/null
        python -c "from splparser.parser import parse; parse('$cmd foo')" &> /dev/null
        echo "OK"
    done
}

pushd ${SPLPARSER_HOME}/splparser/cmdparsers/
generate_parsetabs
popd
