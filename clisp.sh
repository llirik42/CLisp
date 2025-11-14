#!/bin/bash

RED='\033[0;31m'
NC='\033[0m'

if [ ! -d build ]; then
    mkdir build
fi

if [ -f build/out ]; then
    rm build/out
fi

if [[(! -d ./lib)]] || [[(! -f "./lib/libruntime.so") ]]; then
  echo -e "${RED}Error: no runtime library!${NC}"
  echo -e "Execute ./install.sh"
  exit 1
fi

if [ ! -d translator/.venv ]; then
  echo -e "${RED}Error: no translator venv!${NC}"
  echo -e "Execute ./install.sh"
  exit 1
fi

cd translator
if ! .venv/bin/python3 -m src.main -f "../$1" -o "../build/out.c"; then
  exit 1
fi

cd ..
cd build

if ! gcc -o out out.c -I../runtime -L../lib -lruntime -Wl,-rpath,../lib; then
  exit 1
fi

./out
