#copyright Arief Anbiya (2020)
#E-mail: anbarief@live.com

import random
import math

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

color = {0: (0,0,0,0), 2: (0, 0.5, 0, 0.5), 4: (0, 0.5, 0, 1), 8: (0, 1, 0, 0.5), \
         16: (0, 1, 0, 1), 32: (0, 0, 0.5, 0.5), 64: (0, 0, 0.5, 1), 128: (0, 0, 1, 0.5), \
         256: (0, 0, 1, 1), 512: (0.75, 0, 0, 0.5), 1024: (0.75, 0, 0, 1), 2048: (1, 0, 0, 1)}


class App2048:

    def __init__(self, n):
        self.n = n

        self.fig, self.axes = plt.subplots()

        self.axes.axis('scaled')

        self.axes.set_xlim(0, n+1); self.axes.set_ylim(0, n+1)

        self.cells = []
        for i in range(1,n+1):
            row_cells = []
            for j in range(1, n+1):
                cell = CellObject(i, j, 0, \
                                  self.fig, self.axes)
                row_cells.append(cell)
            self.cells.append(row_cells)

        self.cells_2 = []
        for row in self.cells:
            self.cells_2.extend(row)

        c1 = random.sample(self.cells_2, 1)[0]
        c2 = random.sample(self.cells_2, 1)[0]
        while c2 == c1:
            c2 = random.sample(self.cells_2, 1)[0]
            
        c1.value = 2; c1.update()
        c2.value = 2; c2.update()

        self.connect()

        self.press = False
        self.path = []
        self.win = False
        plt.show()

    def on_press(self, event):
        pos = event.xdata, event.ydata
        if None not in pos:
            self.press = True
            self.path.append(pos)

    def on_motion(self, event):
        if self.press:
            pos = event.xdata, event.ydata
            if None not in pos:
                self.path.append(pos)
            else:
                self.path.clear()
                self.press = False
                return None

            dx = self.path[-1][0] - self.path[0][0]
            dy = self.path[-1][1] - self.path[0][1]
            vector_length = math.sqrt((dx**2) + (dy**2))

            direction = None
            if vector_length >= 0.5:
                if abs(dx) > abs(dy):
                    if dx > 0:
                        direction = 'right'
                    elif dx < 0:
                        direction = 'left'
                elif abs(dy) > abs(dx):
                    if dy > 0:
                        direction = 'up'
                    elif dy < 0:
                        direction = 'down'
            if direction != None:
                self.press = False
                self.path.clear()

                previous_values = self.values

                if direction == 'up':
                    self.go_up()
                elif direction == 'down':
                    self.go_down()
                elif direction == 'right':
                    self.go_right()
                else:
                    self.go_left()

                if self.changed(previous_values):
                    self.add_new_value()

                self.solved_or_lost()

    def on_release(self, event):
        pos = event.xdata, event.ydata
        self.press = False
        self.path.clear()

    def solvable(self):
        current_values = self.values
        if 0 in current_values:
            return True
        else:
            for i in range(self.n):
                for j in range(self.n):
                    if j+1 <= self.n-1:
                        if self.cells[i][j].value == self.cells[i][j+1].value:
                            return True
                    if 0 <= j-1:
                        if self.cells[i][j].value == self.cells[i][j-1].value:
                            return True

                    if i+1 <= self.n-1:
                        if self.cells[i][j].value == self.cells[i+1][j].value:
                            return True

                    if 0 <= i-1:
                        if self.cells[i][j].value == self.cells[i-1][j].value:
                            return True

    def solved_or_lost(self):
        current_values = self.values
        if (2048 in current_values) and (not self.win):
            self.axes.set_title('WIN', color= 'blue')
            self.fig.canvas.draw()
            self.win = True
            return True
        elif self.solvable():
            return False
        else:
            self.axes.set_title('LOSE', color = 'red')
            self.fig.canvas.draw()
            plt.pause(2)
            plt.close()
            
    @property
    def values(self):
        return [cell.value for cell in self.cells_2] 

    def changed(self, previous_values):
        current_values = self.values
        return current_values != previous_values

    def add_new_value(self):
        new_number = random.sample([2,2,2,2,2,2,2,4,4,4], 1)[0]
        random_cell = random.sample([cell for cell in self.cells_2 if cell.value==0], \
                                    1)[0]
        random_cell.value = new_number
        random_cell.update(draw=True)
        
    def go_up(self):
        for j in range(self.n):
            positives = [self.cells[self.n-1-i][j].value for i in range(self.n) if self.cells[self.n-1-i][j].value > 0]
            for i in range(self.n):
                self.cells[i][j].value = 0; self.cells[i][j].update(draw=False)
            for i in range(len(positives)):
                self.cells[self.n-1-i][j].value = positives[i]; self.cells[self.n-1-i][j].update(draw=False)            
        self.fig.canvas.draw()

        for j in range(self.n):
            positives = [self.cells[self.n-1-i][j] for i in range(self.n) if self.cells[self.n-1-i][j].value > 0]
            for i in range(len(positives)-1):
                if self.cells[self.n-1-i][j].value == self.cells[self.n-2-i][j].value:
                    self.cells[self.n-1-i][j].value = 2*self.cells[self.n-2-i][j].value
                    self.cells[self.n-2-i][j].value = 0
                    self.cells[self.n-1-i][j].update(draw=False); self.cells[self.n-2-i][j].update(draw=False)
            positives = [self.cells[self.n-1-i][j].value for i in range(self.n) if self.cells[self.n-1-i][j].value > 0]
            for i in range(self.n):
                self.cells[i][j].value = 0; self.cells[i][j].update(draw=False)
            for i in range(len(positives)):
                self.cells[self.n-1-i][j].value = positives[i]; self.cells[self.n-1-i][j].update(draw=False)              
        self.fig.canvas.draw()

    def go_down(self):
        for j in range(self.n):
            positives = [self.cells[i][j].value for i in range(self.n) if self.cells[i][j].value > 0]
            for i in range(self.n):
                self.cells[i][j].value = 0; self.cells[i][j].update(draw=False)
            for i in range(len(positives)):
                self.cells[i][j].value = positives[i]; self.cells[i][j].update(draw=False)
        self.fig.canvas.draw()

        for j in range(self.n):
            positives = [self.cells[i][j] for i in range(self.n) if self.cells[i][j].value != 0]
            for i in range(len(positives)-1):
                if self.cells[i][j].value == self.cells[i+1][j].value:
                    self.cells[i][j].value = 2*self.cells[i+1][j].value
                    self.cells[i+1][j].value = 0
                    self.cells[i][j].update(draw=False); self.cells[i+1][j].update(draw=False)
            positives = [self.cells[i][j].value for i in range(self.n) if self.cells[i][j].value > 0]
            for i in range(self.n):
                self.cells[i][j].value = 0; self.cells[i][j].update(draw=False)
            for i in range(len(positives)):
                self.cells[i][j].value = positives[i]; self.cells[i][j].update(draw=False)        
        self.fig.canvas.draw()

    def go_left(self):
        for i in range(self.n):
            positives = [self.cells[i][j].value for j in range(self.n) if self.cells[i][j].value > 0]
            for j in range(self.n):
                self.cells[i][j].value = 0; self.cells[i][j].update(draw=False)
            for j in range(len(positives)):
                self.cells[i][j].value = positives[j]; self.cells[i][j].update(draw=False)
        self.fig.canvas.draw()

        for i in range(self.n):
            positives = [self.cells[i][j] for j in range(self.n) if self.cells[i][j].value > 0]
            for j in range(len(positives)-1):
                if self.cells[i][j].value == self.cells[i][j+1].value:
                    self.cells[i][j].value = 2*self.cells[i][j+1].value
                    self.cells[i][j+1].value = 0
                    self.cells[i][j].update(draw=False); self.cells[i][j+1].update(draw=False)
            positives = [self.cells[i][j].value for j in range(self.n) if self.cells[i][j].value > 0]
            for j in range(self.n):
                self.cells[i][j].value = 0; self.cells[i][j].update(draw=False)
            for j in range(len(positives)):
                self.cells[i][j].value = positives[j]; self.cells[i][j].update(draw=False)
        self.fig.canvas.draw() 

    def go_right(self):
        for i in range(self.n):
            positives = [self.cells[i][self.n-1-j].value for j in range(self.n) if self.cells[i][self.n-1-j].value > 0]
            for j in range(self.n):
                self.cells[i][j].value = 0; self.cells[i][j].update(draw=False)
            for j in range(len(positives)):
                self.cells[i][self.n-1-j].value = positives[j]; self.cells[i][self.n-1-j].update(draw=False)
        self.fig.canvas.draw()

        for i in range(self.n):
            positives = [self.cells[i][self.n-1-j] for j in range(self.n) if self.cells[i][self.n-1-j].value > 0]
            for j in range(len(positives)-1):
                if self.cells[i][self.n-1-j].value == self.cells[i][self.n-2-j].value:
                    self.cells[i][self.n-1-j].value = 2*self.cells[i][self.n-2-j].value
                    self.cells[i][self.n-2-j].value = 0
                    self.cells[i][self.n-1-j].update(draw=False); self.cells[i][self.n-2-j].update(draw=False)
            positives = [self.cells[i][self.n-1-j].value for j in range(self.n) if self.cells[i][self.n-1-j].value > 0]
            for j in range(self.n):
                self.cells[i][j].value = 0; self.cells[i][j].update(draw=False)
            for j in range(len(positives)):
                self.cells[i][self.n-1-j].value = positives[j]; self.cells[i][self.n-1-j].update(draw=False)
        self.fig.canvas.draw()

    def connect(self):
        self.fig.canvas.mpl_connect('button_press_event', self.on_press)
        self.fig.canvas.mpl_connect('motion_notify_event', self.on_motion)
        self.fig.canvas.mpl_connect('button_release_event', self.on_release)


class CellObject:

    def __init__(self, row, col, value, fig, axes):
        self.row = row
        self.col = col
        self.value = value
        self.fig, self.axes = fig, axes
        self.start()

    def start(self):
        if self.value == 0:
            self.ec = (0,0,0,0.1)
            self.text_color = (0,0,0,0)
        else:
            self.ec = (0,0,0,1)
            self.text_color = (1,1,1,1)

        self.fc = color[self.value]
        
        self.center = [self.col, self.row]

        self.rect = Rectangle([self.col-0.5, self.row-0.5], \
                              width = 1, height = 1, fc = self.fc, ec = self.ec, \
                              linewidth = 2)

        self.text = self.axes.text(self.col, self.row, str(self.value), \
                                   color = self.text_color, \
                                   ha = 'center', va = 'center', \
                                   fontweight = 'bold')

        self.axes.add_patch(self.rect)
        self.fig.canvas.draw()

    def update(self, draw = False):
        if self.value == 0:
            self.ec = (0,0,0,0.1)
            self.text_color = (0,0,0,0)
        else:
            self.ec = (0,0,0,1)
            self.text_color = (1,1,1,1)

        self.fc = color[min(self.value, 2048)]
        self.rect.set_fc(self.fc)
        self.rect.set_ec(self.ec)
        self.text.set_color(self.text_color)
        self.text.set_text(str(self.value))

        if draw:
            self.fig.canvas.draw()

if __name__ == '__main__':
    n = 4
    app = App2048(n)
