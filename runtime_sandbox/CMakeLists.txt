cmake_minimum_required(VERSION 3.10)
project(sandbox C)

set(CMAKE_C_STANDARD 11)

include_directories(../runtime)

add_executable(sandbox main.c)

target_link_libraries(sandbox PRIVATE ${CMAKE_CURRENT_SOURCE_DIR}/../lib/libruntime.so)