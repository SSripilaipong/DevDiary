#!/bin/sh -l

apk add --update make

cd $1
make test-unit
make test-usecase
