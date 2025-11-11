#!/bin/bash

if [ ! -d translator/.venv ]; then
    cd translator/
    uv venv
    source .venv/bin/activate
    uv sync
    deactivate
    cd ..
fi

if ! ./antlr_generate.sh; then
  exit 1
fi

if ! ./compile_runtime_lib.sh; then
  exit 1
fi
