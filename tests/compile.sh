#!/bin/bash

filename=$(basename "$1")

gcc -o "build/${filename%.*}" $1 -I../runtime -L../lib -lruntime -Wl,-rpath,../lib
