#!/bin/bash

echo "rm logs/* 2> /dev/null"
rm logs/* 2> /dev/null
echo "rm parsetabs/* 2> /dev/null"
rm parsetabs/* 2> /dev/null
echo "rm -rf build/ 2> /dev/null"
rm -rf build/ 2> /dev/null
echo "rm -rf dist/ 2> /dev/null"
rm -rf dist/ 2> /dev/null
