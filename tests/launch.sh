#!/bin/bash

RED='\033[0;31m'
NC='\033[0m'

if [ ! -d .venv ]; then
    uv venv
    source .venv/bin/activate
    uv sync
    deactivate
fi

if [ ! -d build ]; then
    mkdir build
fi

if ! ../install.sh &> /dev/null; then
  echo -e "${RED}Error during installing!${NC}"
  exit 1
fi

rm -rf ./build/*

.venv/bin/pytest -s main.py

rm -rf ./build/*