cmake_minimum_required(VERSION 3.20)
project(runtime C)

set(CMAKE_C_STANDARD 11)

add_executable(out out.c runtime.c)
