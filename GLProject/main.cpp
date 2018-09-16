#include <stdio.h>
#include <stdlib.h>

//Include GLEW. Always include it before gl.h and glfw3.h, since it's a big magic:
#include <GL/glew.h>

//Window and keyboard stuff:
#include <GLFW/glfw3.h>

//Include 3D Math library:
#include <glm/glm.hpp>
using namespace glm;

//Array of 3D vectors to represent 3D vertices:
static const GLfloat g_vertex_buffer_data[] = {
    -1.0f,-1.0f,0.0f,
    1.0f,-1.0f,0.0f,
    0.0f,1.0f,0.0f,
};

void error_callback(int error, const char* description)
{
    puts(description);
}

GLFWwindow* setupScreen(void);

//Routine defining what happens before window is closed:
void loop(GLFWwindow * window);

int main()
{
    GLFWwindow * window = setupScreen();

    //Dark blue background:
    glClearColor(0.0f,0.0f,0.4f,0.0f);

    GLuint VertexArrayID;
    glGenVertexArrays(1,&VertexArrayID);
    glBindVertexArray(VertexArrayID);

    do{
        loop(window);
    }while(glfwGetKey(window,GLFW_KEY_ESCAPE) != GLFW_PRESS && glfwWindowShouldClose(window) == 0);

    return 0;
}

GLFWwindow* setupScreen(void){
    glewExperimental = true; // Needed for core profile
    glfwSetErrorCallback(error_callback);
    if(!glfwInit()){
        printf("Failed to initialize GLFW\n");
        exit(1);
    }

    glfwWindowHint(GLFW_SAMPLES,4); //4x antialiasing

    //We want OpenGL 3.3
    glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR,3);
    glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR,3);
    //etc:
    glfwWindowHint(GLFW_OPENGL_FORWARD_COMPAT,GL_TRUE); //For MacOS purposes only
    glfwWindowHint(GLFW_OPENGL_PROFILE,GLFW_OPENGL_CORE_PROFILE);   //We don't want the old OpenGL

    //Open a window and create its OpenGL context
    GLFWwindow * window = glfwCreateWindow(1024,768,"Tutorial 01",nullptr,nullptr);

    if(window == nullptr){
        printf("Failed to open GLFW window. If you have an Intel GPU, they are not 3.3 compatible.");
        glfwTerminate();
        exit(1);
    }

    glfwMakeContextCurrent(window);
    glewExperimental = true;
    if(glewInit() != GLEW_OK){
        printf("Failed to initialize GLEW\n");
        exit(1);
    }

    glfwSetInputMode(window,GLFW_STICKY_KEYS,GL_TRUE);
    return window;
}

void loop(GLFWwindow * window){
    //Clear the screen, otherwise we might get flickering:
    glClear(GL_COLOR_BUFFER_BIT);

    //Swap buffers
    glfwSwapBuffers(window);
    glfwPollEvents();
}
