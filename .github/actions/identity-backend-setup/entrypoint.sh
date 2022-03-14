#!/bin/sh -l

pwd
ls -la
cd $1
pip install -r requirements.txt --target ./src
cp -r ../lib/chamber ./src
