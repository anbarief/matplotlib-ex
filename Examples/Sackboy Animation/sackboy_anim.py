import math
import random

import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib.animation import FuncAnimation

sophia_regular_otf = "Sofia-Regular.otf"
sophia_regular = fm.FontProperties(fname = sophia_regular_otf, size = 20)

class SackBoyAnim:
    def __init__(self):
        self.fig, self.ax = plt.subplots()

        sackboy_mat = plt.imread("sackboy.png")
        logo_mat = plt.imread("lbp_logo2.png")
        self.sackboy_img = self.ax.imshow(sackboy_mat)
        self.logo_img = self.ax.imshow(logo_mat)
        self.info = " Click anything to change background color."

        extent = self.sackboy_img.get_extent()
        self.sackboy_width = abs(extent[0]-extent[1])
        self.sackboy_height = abs(extent[2]-extent[3])
        new_extent = (extent[0], extent[1], extent[3], extent[2])
        self.sackboy_img.set_extent(new_extent)

        extent = self.logo_img.get_extent()
        self.logo_x = [extent[0], extent[1]*5]; self.logo_y = [extent[3], extent[2]+5*(extent[2]-extent[3])];
        self.logo_width = abs(self.logo_x[0]-self.logo_x[1])
        self.logo_height = abs(self.logo_y[0]-self.logo_y[1])
        new_extent = (self.logo_x[0]+0.5*(self.sackboy_width-self.logo_width), self.logo_x[1]+0.5*(self.sackboy_width-self.logo_width), \
                      self.logo_y[0] +3000, self.logo_y[1] +3000)
        self.logo_img.set_extent(new_extent)

        self.ax.set_xlim([-self.sackboy_width, 2*self.sackboy_width])
        self.ax.set_ylim([0, 2*self.sackboy_height])

        self.text = self.ax.text(0.5*self.sackboy_width, 1.2*self.sackboy_height, self.info, \
                                 fontproperties = sophia_regular, ha = "center", va = "center")
        self.text.set_rotation_mode("anchor")

        self.ax.tick_params(colors = (0,0,0,0))
        self.fig.canvas.mpl_connect('button_press_event', self.onclick)

    def show(self):
        self.fig.show()

    def onclick(self, event):
        new_color = [random.uniform(0,1), random.uniform(0,1), random.uniform(0,1), random.uniform(0,1)]
        self.fig.set_facecolor(new_color)
        self.ax.set_facecolor(new_color)
        

    def animation(self, frame):
        self.text.set_rotation(math.cos(frame)*20)
        
    def animate(self):
        anim = FuncAnimation(self.fig, self.animation, frames = [i*2*math.pi/200 for i in range(201)], \
                             interval = 0.5, repeat = True)
        plt.show(block = True)
        return anim

sackboy = SackBoyAnim()
sackboy.animate()
