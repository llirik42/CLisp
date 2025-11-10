cmake_minimum_required(VERSION 3.20)
project(runtime C)

set(CMAKE_C_STANDARD 11)

file(MAKE_DIRECTORY ${CMAKE_SOURCE_DIR}/build)

set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_SOURCE_DIR}/build)

file(GLOB_RECURSE SOURCE_FILES
        "*.c"
)

add_library(runtime SHARED ${SOURCE_FILES})

set(CMAKE_POSITION_INDEPENDENT_CODE ON)

set_target_properties(runtime PROPERTIES
        OUTPUT_NAME "libruntime"
        PREFIX ""
        SUFFIX ".so"
)
