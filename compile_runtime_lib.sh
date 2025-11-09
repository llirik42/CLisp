#!/bin/bash

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${YELLOW}Начало сборки библиотеки...${NC}"

if [ ! -d "./runtime" ]; then
    echo -e "${RED}Ошибка: Папка './runtime' не найдена!${NC}"
    exit 1
fi

if [ ! -f "./runtime/CMakeLists.txt" ]; then
    echo -e "${RED}Ошибка: Файл './runtime/CMakeLists.txt' не найден!${NC}"
    exit 1
fi

if [ -z "$(find ./runtime -name '*.c' -print -quit)" ]; then
    echo -e "${RED}Ошибка: В папке './runtime' не найдены .c файлы!${NC}"
    exit 1
fi

if ! command -v cmake &> /dev/null; then
    echo -e "${RED}Ошибка: CMake не установлен!${NC}"
    exit 1
fi

cd ./runtime

if [ ! -d "./build" ]; then
    echo -e "${YELLOW}Создание директории ./runtime/build ...${NC}"
    mkdir -p build
fi

cd ./build

echo -e "${YELLOW}Запуск CMake из папки ./runtime ...${NC}"
cmake ..

if [ $? -ne 0 ]; then
    echo -e "${RED}Ошибка при выполнении CMake!${NC}"
    exit 1
fi

echo -e "${YELLOW}Компиляция библиотеки...${NC}"
make

if [ $? -eq 0 ]; then
  echo -e "${GREEN}Сборка успешно завершена!${NC}"

  COMPILED_LIB_PATH='./libruntime.so'

  if [ -f ${COMPILED_LIB_PATH} ]; then
      echo -e "${GREEN}Библиотека успешно создана ${NC}"
  else
      echo -e "${RED}Ошибка: Библиотека не была создана!${NC}"
      exit 1
  fi

  cd ../../

  if [ ! -d "./lib" ]; then
      echo -e "${YELLOW}Создание директории ./lib ...${NC}"
      mkdir -p ./lib
  fi

  echo -e "${YELLOW}Перемещение библиотеки в папку ./lib ...${NC}"

  if [ -f "./lib/${COMPILED_LIB_PATH}" ]; then
      rm "./lib/${COMPILED_LIB_PATH}"
  fi

  mv "./runtime/build/${COMPILED_LIB_PATH}" "./lib/${COMPILED_LIB_PATH}"

  if [ -f "./lib/${COMPILED_LIB_PATH}" ]; then
    echo -e "${GREEN}Библиотека успешно перемещена в папку ./lib${NC}"
  else
    echo -e "${RED}Ошибка при перемещении библиотеки${NC}"
    exit 1
  fi

  exit 0

else
  echo -e "${RED}Ошибка при компиляции!${NC}"
  exit 1
fi
