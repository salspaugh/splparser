#!/bin/bash

python setup.py bdist_egg upload
python setup.py bdist_wininst register upload
python setup.py sdist upload
