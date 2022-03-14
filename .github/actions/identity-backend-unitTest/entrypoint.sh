#!/bin/sh -l

cd $1
make test-unit
make test-usecase
