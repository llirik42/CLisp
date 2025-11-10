#!/bin/bash

ANTLR_JAR="/usr/local/lib/antlr-4.13.2-complete.jar"
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

cd ./translator

if java -Xmx500M -cp "$ANTLR_JAR:$CLASSPATH" org.antlr.v4.Tool -Dlanguage=Python3 -visitor -o src Lisp.g4; then
  echo -e "${GREEN}Successful generated code by ANTLR4${NC}"
else
  echo -e "${RED}Error during generating code by ANTLR4!${NC}"
  exit 1
fi
