IF(MSVC)
	# msvc wants to "deprecate" standard C. Turn those warnings off.
	add_definitions(-D_CRT_SECURE_NO_WARNINGS)
	add_definitions(-D_CRT_NONSTDC_NO_DEPRECATE)

	SET(LIBTCOD_NAME libtcod-VS)
	SET(SDL_NAME SDL)
	SET(ZLIB_NAME zdll)
ELSEIF(MINGW)
	SET(LIBTCOD_NAME tcod-mingw)
	SET(SDL_NAME SDL)
	SET(ZLIB_NAME z)
ELSEIF(APPLE)
	SET(LIBTCOD_NAME tcod)
	find_package(SDL REQUIRED)
	SET(SDL_NAME ${SDL_LIBRARY})
	SET(ZLIB_NAME z)
ELSEIF(UNIX)
	SET(LIBTCOD_NAME tcod)
	SET(SDL_NAME SDL)
	SET(ZLIB_NAME z)
ENDIF()

SET(LIBTCOD_C_SRC bresenham_c.c bsp_c.c color_c.c console_c.c fov_c.c fov_circular_raycasting.c 
				fov_diamond_raycasting.c fov_permissive.c fov_permissive2.c fov_recursive_shadowcasting.c 
				fov_restrictive.c heightmap_c.c image_c.c lex_c.c list_c.c mersenne_c.c namegen_c.c 
				noise_c.c parser_c.c path_c.c sys_c.c sys_sdl_c.c sys_sdl_img_bmp.c 
				sys_sdl_img_png.c tree_c.c txtfield_c.c wrappers.c zip_c.c)


IF(APPLE)
SET(LIBTCOD_C_SRC ${LIBTCOD_C_SRC} ../osx/macsupport.m)
ENDIF()

SET(PNG_NAME png15_static)
include_directories(../dependencies/libpng-1.5.6)

# Linux wants seperate C and C++ libraries.
IF(UNIX AND NOT APPLE)
	add_library(${LIBTCOD_NAME} SHARED ${LIBTCOD_C_SRC})
	target_link_libraries(${LIBTCOD_NAME} ${PNG_NAME} ${SDL_NAME} ${ZLIB_NAME} ${M_LIB} ${EFENCE_LIBRARY} X11)

ELSE()
	add_library(${LIBTCOD_NAME} SHARED ${LIBTCOD_C_SRC}) 
	target_link_libraries(${LIBTCOD_NAME} ${PNG_NAME} ${SDL_NAME} ${ZLIB_NAME} ) 
ENDIF()

set(LIBTCOD_NAME_STATIC ${LIBTCOD_NAME}_static)
add_library(${LIBTCOD_NAME_STATIC} STATIC ${LIBTCOD_C_SRC})


IF(MINGW)
	target_link_libraries(${LIBTCOD_NAME} dxguid winmm)
ENDIF()

IF(MSVC OR MINGW)
	# Since we're exporting functions and clases, we use the "standard" macro combinations to do so under msvc.
	# These turn them on for the right builds.
	set_property(TARGET ${LIBTCOD_NAME} PROPERTY COMPILE_DEFINITIONS LIBTCOD_EXPORTS)
ENDIF()

IF(MSVC)
	# Since libtcod pulls in DLLs that use the release CRT, force the linker to never try to cross match CRTs
	set_property(TARGET ${LIBTCOD_NAME} PROPERTY LINK_FLAGS "/NODEFAULTLIB:MSVCRTD.lib ")
ENDIF()

set_property(TARGET ${LIBTCOD_NAME} PROPERTY DEBUG_POSTFIX "-debug")

IF(UNIX)
	SET(CMAKE_SHARED_LIBRARY_LINK_C_FLAGS "") #Workaround for -rdynamic
	SET(CMAKE_SHARED_LIBRARY_LINK_CXX_FLAGS "") #same

	SET(CMAKE_SKIP_RPATH ON) #Don't place hard coded rpaths'
	SET(CMAKE_SHARED_LINKER_FLAGS "-Wl,-rpath,. ${CMAKE_SHARED_LINKER_FLAGS}")
ENDIF()

INSTALL(TARGETS ${LIBTCOD_NAME} ${LIBTCOD_NAME_STATIC}
  RUNTIME DESTINATION ${INSTALL_DIR}
  LIBRARY DESTINATION ${INSTALL_DIR}
  ARCHIVE DESTINATION ${INSTALL_DIR}
)
