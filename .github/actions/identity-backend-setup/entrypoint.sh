#!/bin/sh -l

cd $1
pip install -r requirements.txt --target ./src
cp -r ../lib/chamber/chamber ./src
cp -r ../lib/lambler/lambler ./src
