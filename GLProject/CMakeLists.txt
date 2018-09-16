cmake_minimum_required(VERSION 2.8)

project(GLProject)

find_package(OpenGL REQUIRED)
#find_package(GLEW REQUIRED)
#find_package(glfw3 REQUIRED)

set(ALL_LIBS
        ${OPENGL_LIBRARIES}
        glfw
        GLEW
)

add_definitions(
        -DTW_STATIC
        -DTW_NO_LIB_PRAGMA
        -DTW_NO_DIRECT3D
        -DGLEW_STATIC
        -D_CRT_SECURE_NO_WARNINGS
)

#include_directories(${OPENGL_INCLUDE_DIR} ${GLEW_INCLUDE_DIRS})
#include_directories(${OPENGL_INCLUDE_DIR} ${glfw3_INCLUDE_DIRS})

add_executable(test
    main.cpp
    shader.cpp
    shader.hpp

    simplevertexshader.vertexshader
    simplefragmentshader.fragmentshader
)

#target_link_libraries(test ${OPENGL_LIBRARIES} ${GLEW_LIBRARIES} ${glfw3_LIBRARIES})
target_link_libraries(test ${ALL_LIBS})

#add_executable(${PROJECT_NAME} "main.cpp")
