
SET(LIBSOUND_C_SRC libsound.cc)

include_directories(../liblo/)
include_directories(../liblo/lo)
include_directories(../libtcod/include)

SET(LIBLO_NAME lo_static)
SET(LIBSOUND_NAME sound)

add_library(${LIBSOUND_NAME} SHARED ${LIBSOUND_C_SRC})
target_link_libraries(${LIBSOUND_NAME} ${LIBLO_NAME})


IF(MINGW)
	target_link_libraries(${LIBSOUND_NAME} ws2_32)
ENDIF()

###

SET(LIBDIGGR_C_SRC libdiggr.cc)

SET(LIBDIGGR_NAME diggr)

add_library(${LIBDIGGR_NAME} SHARED ${LIBDIGGR_C_SRC})
target_link_libraries(${LIBDIGGR_NAME} tcod_static)

IF(UNIX AND NOT APPLE)
	target_link_libraries(${LIBDIGGR_NAME} png15_static SDL m X11)

ELSE()
	target_link_libraries(${LIBDIGGR_NAME} png15_static SDL) 
ENDIF()

IF(MINGW)
	target_link_libraries(${LIBDIGGR_NAME} dxguid winmm)
ENDIF()



INSTALL(TARGETS ${LIBSOUND_NAME} ${LIBDIGGR_NAME}
  RUNTIME DESTINATION ${INSTALL_DIR}
  LIBRARY DESTINATION ${INSTALL_DIR}
  ARCHIVE DESTINATION ${INSTALL_DIR}
)

