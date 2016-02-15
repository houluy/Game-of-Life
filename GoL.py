import pyglet
import math

LENGTH=800
HEIGHT=800
FRAME_L = 600
FRAME_H = 600
CELL_LEIGHT = 50
CELL_HEIGHT = 50
POINT_NUMBER = 11
RADIUS = 10

game_window = pyglet.window.Window(LENGTH, HEIGHT)

#pyglet.clock.schedule_interval(update, 1/120.0)

def generate_circle(heart, radius):
    x0 = [heart[0] - radius + t*2*radius/(POINT_NUMBER - 1) for t in range(POINT_NUMBER)]
    x0.reverse()
    x1 = x0[1:-1]
    x0.reverse()
    y0 = [math.sqrt(radius**2 - (t - heart[0])**2) + heart[1] for t in x0]
    y1 = [2*heart[1] - t for t in y0[1:-1]]
    cor = []
    for i in range(len(x0)):
        cor.append(x0[i])
        cor.append(y0[i])
    for i in range(len(x1)):
        cor.append(x1[i])
        cor.append(y1[i])
    return cor

class Cell:
    def __init__(self, x, y, state):
        self.x = x
        self.y = y
        self._tranverse()
        self.old_state = state
        self.new_state = state
    def change_state(self):
        self.state = 0 if self.state == 1 else 1
    def _tranverse(self):
        self.cor_x = RADIUS*(2*self.x - 1)
        self.cor_y = RADIUS*(2*self.y - 1)

    def draw(self):
        cord = generate_circle((self.cor_x, self.cor_y), RADIUS)
        pyglet.graphics.draw(POINT_NUMBER*2 - 2, pyglet.gl.GL_LINE_LOOP, ('v2f', tuple(cord)))

@game_window.event
def on_draw():
    game_window.clear()
    cell = Cell(1,1,1)
    cell.draw()    

if __name__ == '__main__':
    pyglet.app.run()



