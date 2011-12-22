cmake_minimum_required (VERSION 2.6)
project (libtcod)

SET(CMAKE_BUILD_TYPE "Release")

# All projects need "include" directory
include_directories(include)


SET(ROOT_DIR ${CMAKE_CURRENT_SOURCE_DIR})
#SET(INSTALL_DIR ${CMAKE_CURRENT_SOURCE_DIR})

IF(MSVC)
	SET(LIBTCOD_NAME libtcod-VS)
	SET(LIB_DIR msvc)
ELSEIF(MINGW)
	SET(LIBTCOD_NAME tcod-mingw)
	SET(LIB_DIR mingw)
ELSEIF(APPLE)
	SET(LIBTCOD_NAME tcod)
	SET(LIB_DIR osx)
ELSEIF(UNIX)
	SET(LIBTCOD_NAME tcod)
	SET(LIB_DIR linux)
ENDIF()

find_package(SDL REQUIRED)
#find_package(PNG REQUIRED)
find_package(ZLIB REQUIRED)
find_package(Threads REQUIRED)
find_library(M_LIB m)
IF(CMAKE_BUILD_TYPE MATCHES "Debug")
	find_library(EFENCE_LIBRARY efence PATHS /usr/lib /usr/local/lib)
ENDIF()

SET(PNG_SHARED OFF)
add_subdirectory(dependencies/libpng-1.5.6)
add_subdirectory(src)

