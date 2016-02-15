import pyglet
import math
import random

LENGTH=800
HEIGHT=800
FRAME_L = 600
FRAME_H = 600
CELL_LENGTH = 50
CELL_HEIGHT = 50
POINT_NUMBER = 11
RADIUS = 10
cell_dict = {}
game_window = pyglet.window.Window(LENGTH, HEIGHT)


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

def generate_cross(heart, radius):
    x0 = heart[0] - radius
    y0 = heart[1] - radius
    x1 = heart[0] + radius
    y1 = heart[1] + radius
    x2 = heart[0] - radius
    y2 = heart[1] + radius
    x3 = heart[0] + radius
    y3 = heart[1] - radius
    return [x0, y0, x1, y1, x2, y2, x3, y3]    


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
        self.cor_x = RADIUS*(2*self.x + 1)
        self.cor_y = RADIUS*(2*self.y + 1)

    def draw(self):
        if self.old_state == 1:
            cord = generate_circle((self.cor_x, self.cor_y), RADIUS)
            pyglet.graphics.draw(POINT_NUMBER*2 - 2, pyglet.gl.GL_LINE_LOOP, ('v2f', tuple(cord)))
        elif self.old_state == 0:
            pass
    
    def get_pos(self):
        return (self.x, self.y)

    def get_state(self):
        return self.old_state

    def live(self):
        if self.old_state == 0:
            self.new_state = 1
    def die(self):
        if self.old_state == 1:
            self.new_state = 0
    def update(self):
        self.old_state = self.new_state
#cord = generate_cross((self.cor_x, self.cor_y), RADIUS)
#           pyglet.graphics.draw(2, pyglet.gl.GL_LINES, ('v2f', tuple(cord[0:4])))
#           pyglet.graphics.draw(2, pyglet.gl.GL_LINES, ('v2f', tuple(cord[4:8])))

@game_window.event
def on_draw():
    game_window.clear()
    for i in range(CELL_LENGTH):
       for j in range(CELL_HEIGHT):
          cell_dict[(i, j)].draw() 

def update(dt):
    for i in range(CELL_LENGTH):
        for j in range(CELL_HEIGHT):
            cell = cell_dict[(i, j)]
            lives = check_lives(cell)
            if lives == 2:
                continue
            elif lives == 3:
                cell.live()
            else:
                cell.die()
    for i in range(CELL_LENGTH):
        for j in range(CELL_HEIGHT):
            cell_dict[(i, j)].update()

def check_lives(cell):
    x, y = cell.get_pos()
    lives = 0
    surroundings = [(x - 1, y - 1), (x - 1, y), (x - 1, y + 1), (x, y - 1), (x, y + 1), (x + 1, y - 1), (x + 1, y), (x + 1, y + 1)]
    for i in range(len(surroundings)):
        if surroundings[i][0] < 0 or surroundings[i][0] > CELL_LENGTH - 1 or surroundings[i][1] < 0 or surroundings[i][1] > CELL_HEIGHT - 1:
            surroundings[i] = 0
    for i in surroundings:
        if i != 0:
           if cell_dict[i].get_state() == 1:
               lives += 1 
    return lives

pyglet.clock.schedule_interval(update, 1/120.0)
if __name__ == '__main__':
    for i in range(CELL_LENGTH):
        for j in range(CELL_HEIGHT):
            state = random.randint(0, 1)
            cell = Cell(i, j, state)
            cell_dict[(i, j)] = cell
    pyglet.app.run()



