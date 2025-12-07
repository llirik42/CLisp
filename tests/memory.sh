#!/bin/bash

RED='\033[0;31m'
NC='\033[0m'
GREEN='\033[0;32m'

export LD_LIBRARY_PATH=../lib:$LD_LIBRARY_PATH

for file in $(find . -type f -name "*.out"); do
    if ! valgrind --leak-check=full --error-exitcode=1 "$file" > /dev/null 2>&1; then
        echo -e "${RED}Memory problems in $file${NC}"
    else
        echo -e "${GREEN}No memory problems in $file${NC}"
    fi
done
