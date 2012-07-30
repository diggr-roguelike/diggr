
cmake_minimum_required (VERSION 2.6)
project (diggr)

SET(CMAKE_BUILD_TYPE "Release")

SET(CMAKE_CXX_FLAGS "-Wall -std=c++0x -O3 -g -pthread")

#include_directories(include)

SET(ROOT_DIR ${CMAKE_CURRENT_SOURCE_DIR})
SET(INSTALL_DIR ${CMAKE_CURRENT_SOURCE_DIR}/dist)

add_subdirectory(libtcod)
add_subdirectory(liblo)
add_subdirectory(future)
add_subdirectory(netgame)

### ### ###


SET(PY_SOURCES celauto.py features.py items.py monsters.py moon.py sounds.py vaults.py 
               achievements.py coeffs.py dgsys.py flair.py inventory.py 
               messages.py quests.py stats.py xy.py scores.py libdiggrpy.py)

SET(OTHER_FILES font.png diggr.cfg README BUILD_INSTRUCTIONS GUIDE.txt)

INSTALL(FILES ${PY_SOURCES} DESTINATION ${INSTALL_DIR})
INSTALL(FILES ${OTHER_FILES} DESTINATION ${INSTALL_DIR})

if(WIN32)

  INSTALL(FILES diggr.pyw diggr-replayer.pyw diggr-py2exe.py 
                Rock-Collecting.ico 
          DESTINATION ${INSTALL_DIR})

else()

  INSTALL(FILES diggr.pyw DESTINATION ${INSTALL_DIR}
          RENAME diggr.py)

  INSTALL(FILES diggr-replayer.pyw DESTINATION ${INSTALL_DIR}
          RENAME diggr-replayer.py)

  INSTALL(PROGRAMS unixscripts/diggr unixscripts/diggr-replayer DESTINATION ${INSTALL_DIR})

endif()

INSTALL(DIRECTORY "sound/synths/" DESTINATION "${INSTALL_DIR}/sound/synths")

INSTALL(CODE "FILE(MAKE_DIRECTORY ${INSTALL_DIR}/replays)")

#IF("${arch_hint}" STREQUAL "x64")
#  INSTALL(PROGRAMS unixscripts/diggr-fix-glibc unixscripts/diggr-replayer-fix-glibc ${INSTALL_DIR})
#ENDIF()


# TODO:
# copy libc-2.15.so

# Set up a minimum Supercollider build.

option(SC_QT "" OFF)
option(FFT_GREEN "" ON)
option(NO_LIBSNDFILE "" ON)
option(SUPERNOVA "" OFF)
option(NO_AVAHI "" ON)
option(SC_WII "" OFF)
option(SC_EL "" OFF)
option(SC_ED "" OFF)
option(SC_VIM "" OFF)
option(SC_PSYCOLLIDER "" OFF)

# CMake suxx. Why is that in the year 2012 we are still forced to
# put up with this idiocy?

get_filename_component(CWD "${CMAKE_SOURCE_DIR}" ABSOLUTE)
set(CMAKE_SOURCE_DIR "${CWD}/supercollider")

if(MINGW)
  set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -U__STRICT_ANSI__")
endif()

add_subdirectory("supercollider/" EXCLUDE_FROM_ALL)

# TODO: Prune this list, as not everything here is useful/needed.
set(plugins_list 
        BinaryOpUGens
        ChaosUGens
        DelayUGens
        DemandUGens
        DynNoiseUGens
        FilterUGens
        GendynUGens
        GrainUGens
        IOUGens
        LFUGens
        MulAddUGens
        NoiseUGens
        OscUGens
        PanUGens
        PhysicalModelingUGens
        ReverbUGens
        TestUGens
        TriggerUGens
        UnaryOpUGens
        UnpackFFTUGens

        MouseUGens KeyboardUGens FFT_UGens PV_ThirdParty ML_UGens
)

# I have to set this propery again, due to CMake being braindead about recursion. 
# FFfffuuuuu....
#set_property(TARGET ${plugins_list} APPEND PROPERTY COMPILE_DEFINITIONS NO_LIBSNDFILE)

#if(MINGW)
#  set_property(TARGET libscsynth APPEND PROPERTY COMPILE_DEFINITIONS "SC_PLUGIN_LOAD_SYM=\"\"")
#endif()

add_custom_target(scsynth_fake ALL DEPENDS scsynth)
add_custom_target(plugins_fake ALL DEPENDS ${plugins_list})

install(DIRECTORY "${CMAKE_BINARY_DIR}/supercollider/server/scsynth/" 
        DESTINATION "${INSTALL_DIR}/sound"
        USE_SOURCE_PERMISSIONS
        FILES_MATCHING PATTERN "*scsynth*"
        REGEX "CMakeFiles" EXCLUDE)

install(DIRECTORY "${CMAKE_BINARY_DIR}/supercollider/server/plugins/"
        DESTINATION "${INSTALL_DIR}/sound/plugins"
        USE_SOURCE_PERMISSIONS
        FILES_MATCHING REGEX "Gens|ThirdParty"
        REGEX "CMakeFiles" EXCLUDE)

# CMake does not allow this. FFffuuuu....
#install(TARGETS supercollider/scsynth DESTINATION "${INSTALL_DIR}/sound")
#install(TARGETS ${plugins_list} DESTINATION "${INSTALL_DIR}/sound/plugins")
