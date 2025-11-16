#!/bin/bash

cd "$(dirname "${BASH_SOURCE[0]}")"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${YELLOW}Starting to build the library...${NC}"

if [ ! -d "./runtime" ]; then
    echo -e "${RED}Error: directory './runtime' not found!${NC}"
    exit 1
fi

if [ ! -f "./runtime/CMakeLists.txt" ]; then
    echo -e "${RED}Error: file './runtime/CMakeLists.txt' not found!${NC}"
    exit 1
fi

if [ -z "$(find ./runtime -name '*.c' -print -quit)" ]; then
    echo -e "${RED}Error: in directory './runtime' not found .c files!${NC}"
    exit 1
fi

if ! command -v cmake &> /dev/null; then
    echo -e "${RED}Error: CMake not installed!${NC}"
    exit 1
fi

cd ./runtime

if [ ! -d "./build" ]; then
    echo -e "${YELLOW}Creating directory ./runtime/build ...${NC}"
    mkdir -p build
fi

cd ./build

echo -e "${YELLOW}Launching CMake from directory ./runtime ...${NC}"
cmake ..

if [ $? -ne 0 ]; then
    echo -e "${RED}Error running CMake!${NC}"
    exit 1
fi

echo -e "${YELLOW}Compiling library...${NC}"
make

if [ $? -eq 0 ]; then
  echo -e "${GREEN}Assembly completed successfully.${NC}"

  COMPILED_LIB_PATH='./libruntime.so'

  if [ -f ${COMPILED_LIB_PATH} ]; then
      echo -e "${GREEN}The library has been successfully created.${NC}"
  else
      echo -e "${RED}Error: Library was not created!${NC}"
      exit 1
  fi

  cd ../../

  if [ ! -d "./lib" ]; then
      echo -e "${YELLOW}Creating directory ./lib ...${NC}"
      mkdir -p ./lib
  fi

  echo -e "${YELLOW}Moving the library to the ./lib folder...${NC}"

  if [ -f "./lib/${COMPILED_LIB_PATH}" ]; then
      rm "./lib/${COMPILED_LIB_PATH}"
  fi

  mv "./runtime/build/${COMPILED_LIB_PATH}" "./lib/${COMPILED_LIB_PATH}"

  if [ -f "./lib/${COMPILED_LIB_PATH}" ]; then
    echo -e "${GREEN}The library has been successfully moved to the ./lib folder.${NC}"
  else
    echo -e "${RED}Error moving library!${NC}"
    exit 1
  fi

  exit 0

else
  echo -e "${RED}Compilation error!${NC}"
  exit 1
fi
