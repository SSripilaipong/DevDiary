#!/bin/sh -l

apk add --update make
pip install pytest

cd $1
make test-unit
make test-usecase
