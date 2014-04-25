#!/bin/bash

python -c "from splparser import parse; parse('search foo')" # generates parsetabs 
cp parsetabs/* ${SPLPARSER_HOME}/splparser/parsetabs/

python setup.py bdist_egg upload
python setup.py bdist_wininst register upload
python setup.py sdist upload
