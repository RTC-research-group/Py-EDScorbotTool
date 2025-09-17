#TC_PATH es la ruta de donde se encuentra nuestro compilador para arm
#ROOTFS_PATH es donde tiene que estar descomprimido el sistema de archivos de petalinux para utilizar,
#los archivos comprimidos suelen estar en PROYECTO_PETALINUX/images/linux/rootfs... SE RECOMIENDA UTILIZAR rootfs.tar.bz2
#set( TC_PATH "/usr/bin" )
#set( TC_PATH "/usr/bin/" )
set( TC_PATH "/opt/Xilinx/Petalinux/tools/linux-i386/aarch64-linux-gnu/bin/" )
#set( ROOTFS_PATH "/home/enrique/Escritorio/NPP/rootfs" )
set( ROOTFS_PATH "/home/enrique/Escritorio/prueba/rootfs" )
#set( CROSS_LOCAL_PREFIX "/usr" )

set( CMAKE_SYSTEM_NAME Linux )
set( CMAKE_SYSTEM_PROCESSOR arm )
set(CMAKE_SYSROOT "${ROOTFS_PATH}")

set( CROSS_COMPILE aarch64-linux-gnu- )

set( CMAKE_C_COMPILER "${TC_PATH}${CROSS_COMPILE}gcc" )
set( CMAKE_CXX_COMPILER "${TC_PATH}${CROSS_COMPILE}g++" )
set( CMAKE_LINKER "${TC_PATH}${CROSS_COMPILE}ld" )
set( CMAKE_AR "${TC_PATH}${CROSS_COMPILE}ar" )
set( CMAKE_OBJCOPY "${TC_PATH}${CROSS_COMPILE}objcopy" )

set( CMAKE_FIND_ROOT_PATH_MODE_PROGRAM NEVER )
set( CMAKE_FIND_ROOT_PATH_MODE_LIBRARY ONLY )
set( CMAKE_FIND_ROOT_PATH_MODE_INCLUDE ONLY )
set( CMAKE_FIND_ROOT_PATH_MODE_PACKAGE ONLY )

set( CMAKE_PREFIX_PATH ${ROOTFS_PATH} )
set( CMAKE_INSTALL_PREFIX "${ROOTFS_PATH}${CROSS_LOCAL_PREFIX}" )
set( CMAKE_FIND_ROOT_PATH ${ROOTFS_PATH} )
set( ENV{PKG_CONFIG_PATH} "${ROOTFS_PATH}${CROSS_LOCAL_PREFIX}/lib/pkgconfig/" )
set( ENV{PKG_CONFIG_SYSROOT_DIR} ${ROOTFS_PATH} )

set( CAER_LOCAL_PREFIX ${CROSS_LOCAL_PREFIX} )
set( CAER_LOCAL_INCDIRS "${ROOTFS_PATH}${CROSS_LOCAL_PREFIX}/include/" )
set( CAER_LOCAL_LIBDIRS "${ROOTFS_PATH}/lib/;${ROOTFS_PATH}${CROSS_LOCAL_PREFIX}/lib/" )

SET(CMAKE_INCLUDE_PATH ${CMAKE_INCLUDE_PATH} "/home/enrique/Escritorio/NPP/rootfs/usr/include/boost")