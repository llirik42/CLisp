#!/bin/bash

filename=$1

gcc -o "build/${filename%.*}.out" "build/$1" -I../runtime -L../lib -lruntime -Wl,-rpath,../lib
