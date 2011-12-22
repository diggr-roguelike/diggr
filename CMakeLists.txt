
cmake_minimum_required (VERSION 2.6)
project (diggr)

SET(CMAKE_BUILD_TYPE "Release")

SET(CMAKE_CXX_FLAGS "-std=c++0x")

#include_directories(include)

SET(ROOT_DIR ${CMAKE_CURRENT_SOURCE_DIR})
SET(INSTALL_DIR ${CMAKE_CURRENT_SOURCE_DIR})

add_subdirectory(libtcod)
add_subdirectory(liblo)
add_subdirectory(future)


