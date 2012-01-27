
cmake_minimum_required (VERSION 2.6)
project (diggr)

SET(CMAKE_BUILD_TYPE "Release")

SET(CMAKE_CXX_FLAGS "-std=c++0x")

#include_directories(include)

SET(ROOT_DIR ${CMAKE_CURRENT_SOURCE_DIR})
SET(INSTALL_DIR ${CMAKE_CURRENT_SOURCE_DIR}/dist)

add_subdirectory(libtcod)
add_subdirectory(liblo)
add_subdirectory(future)

### ### ###


SET(PY_SOURCES celauto.py features.py items.py monsters.py moon.py sounds.py vaults.py libdiggrpy.py)

SET(OTHER_FILES font.png diggr.cfg README BUILD_INSTRUCTIONS GUIDE.txt)

INSTALL(FILES ${PY_SOURCES} DESTINATION ${INSTALL_DIR})

INSTALL(FILES diggr.pyw DESTINATION ${INSTALL_DIR}
        RENAME diggr.py)

INSTALL(FILES diggr-replayer.pyw DESTINATION ${INSTALL_DIR}
        RENAME diggr-replayer.py)

INSTALL(FILES ${OTHER_FILES} DESTINATION ${INSTALL_DIR})

INSTALL(PROGRAMS unixscripts/diggr unixscripts/diggr-replayer DESTINATION ${INSTALL_DIR})

IF("${arch_hint}" STREQUAL "x64")
  INSTALL(PROGRAMS unixscripts/diggr-fix-glibc unixscripts/diggr-replayer-fix-glibc ${INSTALL_DIR})
ENDIF()

INSTALL(CODE "FILE(MAKE_DIRECTORY ${INSTALL_DIR}/replays)")

# TODO:
# copy sound/ directory
# copy libc-2.15.so
