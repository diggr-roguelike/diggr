
SET(LIBLO_NAME lo)

add_definitions(-DPACKAGE_NAME="liblo")

add_definitions(-DHAVE_SELECT)

include_directories(..)

if(MINGW)
        add_definitions(-DWINVER=0x0501)
else()
	add_definitions(-DHAVE_INET_ATON)
        add_definitions(-DHAVE_POLL)
        add_definitions(-DHAVE_SYS_SOCKET_H)
endif()

SET(LIBLO_C_SRC   address.c message.c send.c blob.c method.c server.c bundle.c 
                  pattern_match.c server_thread.c timetag.c)

add_library(${LIBLO_NAME} SHARED ${LIBLO_C_SRC})

set(LIBLO_NAME_STATIC ${LIBLO_NAME}_static)
add_library(${LIBLO_NAME_STATIC} STATIC ${LIBLO_C_SRC})

SET_TARGET_PROPERTIES(${LIBLO_NAME_STATIC} PROPERTIES COMPILE_FLAGS -fPIC)


IF(MINGW)
        target_link_libraries(${LIBLO_NAME} ws2_32 pthread wsock32 )
ENDIF()


#INSTALL(TARGETS ${LIBLO_NAME} ${LIBLO_NAME_STATIC}
#  RUNTIME DESTINATION ${INSTALL_DIR}
#  LIBRARY DESTINATION ${INSTALL_DIR}
#  ARCHIVE DESTINATION ${INSTALL_DIR}
#)

