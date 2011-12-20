cmake_minimum_required (VERSION 2.6)
project (liblo)

SET(CMAKE_BUILD_TYPE "Release")

include_directories(lo)

SET(ROOT_DIR ${CMAKE_CURRENT_SOURCE_DIR})
SET(INSTALL_DIR ${CMAKE_CURRENT_SOURCE_DIR})

SET(LIBLO_NAME lo)

find_package(Threads REQUIRED)

add_subdirectory(src)


