#!/bin/bash

ANTLR_JAR="/usr/local/lib/antlr-4.13.2-complete.jar"
RED='\033[0;31m'
NC='\033[0m'
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

if [[(! -d ./lib)]] || [[(! -f "./lib/libruntime.so") ]]; then
  echo -e "${RED}Error: no runtime library!${NC}"
  echo -e "Execute ./compile_runtime_lib.sh"
  exit 1
fi

cd translator
source .venv/bin/activate
python src/main.py -f "../$1" -o "../build/out.c"
deactivate
cd ..

cd build
gcc -o out out.c -I../runtime -L../lib -lruntime -Wl,-rpath,../lib
./out
