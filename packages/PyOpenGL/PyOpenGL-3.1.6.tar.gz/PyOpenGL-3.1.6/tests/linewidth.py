import glfw
from OpenGL.GL import *
if not glfw.init():
    sys.exit()
glfw.window_hint(glfw.SAMPLES, 4)
glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 1)
glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 4)
window = glfw.create_window(800, 600, "Hello World", None, None)
if not window:
    sys.exit()
glfw.make_context_current(window)
glEnable(GL_BLEND)
# glDisable(GL_BLEND)
glClearColor(1.0/255.0*68.0, 1.0/255.0*68.0, 1.0/255.0*68.0, 1.0)
glClear(GL_COLOR_BUFFER_BIT)
glViewport(0, 0, 800, 600)
glMatrixMode(GL_PROJECTION)
glLoadIdentity()
glOrtho(0.0, 800.0, 600.0, 0.0, 0.0, 1.0)
 
def drawOneLine(x1, y1, x2, y2, width):
    glDisable(GL_LINE_SMOOTH);
    glLineWidth(width)
    glBegin(GL_LINES)
    glVertex2f(x1, y1)
    glVertex2f(x2, y2)
    glEnd()
   
if __name__ == "__main__":
    while not glfw.window_should_close(window):
        glfw.poll_events()            
        glClear(GL_COLOR_BUFFER_BIT)
        for y in range(1,20):
            drawOneLine(10,20*y+.5,100,20*y+.5,y*.5)
        glfw.swap_buffers(window)
    glfw.destroy_window(window)
    glfw.terminate()
