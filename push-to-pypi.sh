#!/bin/bash

sh generate_parsetabs.sh

python setup.py bdist_egg upload
python setup.py bdist_wininst register upload
python setup.py sdist upload
