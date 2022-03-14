#!/bin/bash

cd $1
make test-unit
make test-usecase
