cmake_minimum_required(VERSION 3.20)
project(runtime C)

set(CMAKE_C_STANDARD 11)

file(MAKE_DIRECTORY ${CMAKE_SOURCE_DIR}/build)

set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_SOURCE_DIR}/build)

file(GLOB_RECURSE SOURCE_FILES
        "./lib/*.c"
)

add_library(runtime SHARED ${SOURCE_FILES})

set(CMAKE_POSITION_INDEPENDENT_CODE ON)

target_compile_options(runtime PUBLIC -Wall -Werror -Wextra -pedantic)
set_target_properties(runtime PROPERTIES
        OUTPUT_NAME "libruntime"
        PREFIX ""
        SUFFIX ".so"
)
target_include_directories(runtime PUBLIC ${CMAKE_CURRENT_SOURCE_DIR} ${CMAKE_CURRENT_BINARY_DIR} ${CMAKE_CURRENT_SOURCE_DIR}/lib)
target_link_libraries(runtime m)

add_executable(sandbox ${SOURCE_FILES} sandbox/main.c)
target_include_directories(sandbox PRIVATE ${CMAKE_CURRENT_SOURCE_DIR} ${CMAKE_CURRENT_BINARY_DIR} ${CMAKE_CURRENT_SOURCE_DIR}/lib)
target_link_libraries(sandbox m)
