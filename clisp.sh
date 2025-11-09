#!/bin/bash

ANTLR_JAR="/usr/local/lib/antlr-4.13.2-complete.jar"

if [ ! -d translator/.venv ]; then
    cd translator/
    uv venv
    source .venv/bin/activate
    uv sync
    java -Xmx500M -cp "$ANTLR_JAR:$CLASSPATH" org.antlr.v4.Tool -Dlanguage=Python3 -visitor -o src Lisp.g4
    deactivate
    cd ..
fi

if [ ! -d build ]; then
    mkdir build
fi

if [ -f build/out ]; then
    rm build/out
fi

cd translator
source .venv/bin/activate
python src/main.py "../$1" -o "../build/out.c"
deactivate
cd ..

cp runtime/runtime.h runtime/runtime.c build 

cd build
gcc out.c runtime.c -o out
./out
