#Author: Arief Anbiya (2022)
#E-mail: anbarief@live.com

import math
SIN = math.sin
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Button


def adjust_extent(extent):
    return [extent[0]+0.5, extent[1]+0.5, extent[3], extent[2]]

def inbound(pos):
    if (0 <= pos[0] <= 200) and (0 <= pos[1] <= 200):
        return True
    return False

def animate(frame):
    x,y = gundam.pos
    gundam.set_pos(x, y + 0.25*SIN(frame))

    if gundam.thruster.state != 'up':
        if gundam.thruster.anim_count == 5:
            gundam.thruster.anim_count = 0
            gundam.thruster.visible('up')
            gundam.thruster.state = 'up'
        else:
            gundam.thruster.anim_count += 1

    if gundam.img_riflemode_object.get_visible():
        if gundam.anim_count == 10:
            gundam.anim_count = 0
            gundam.visible()
        else:
            gundam.anim_count += 1


class Gundam(object):
    def __init__(self, fname, fname_rifle, ax, pos):
        self.fname = fname
        self.fname_rifle = fname_rifle
        self.anim_count = 0
        self.ax = ax
        self.fig = self.ax.figure
        self.pos = pos
        self.thruster = Thruster(ax, [pos[0]-10, pos[1]-5])
        self.rifle_effect = RifleEffect(ax, pos)
        self.img_matrix = plt.imread(fname)
        self.img_object = ax.imshow(self.img_matrix)

        self.img_riflemode_matrix = plt.imread(fname_rifle)
        self.img_riflemode_object = ax.imshow(self.img_riflemode_matrix, visible=False)

        #calculate dimension:
        default_extent = adjust_extent(self.img_object.get_extent())
        self.dim = default_extent[1]-default_extent[0], default_extent[3]-default_extent[2]

        default_extent = adjust_extent(self.img_riflemode_object.get_extent())
        self.dim_riflemode = default_extent[1]-default_extent[0], default_extent[3]-default_extent[2]
        ##
        
        self.img_object.set_extent(self.extent())
        self.img_riflemode_object.set_extent(self.extent(mode='riflemode'))

    def extent(self, mode='normal'):
        dim = self.dim
        if mode == 'riflemode':
            dim = self.dim_riflemode
        return [self.pos[0]-dim[0]/2, self.pos[0]+dim[0]/2, \
                self.pos[1]-dim[0]/2, self.pos[1]+dim[1]/2]

    def visible(self, mode='normal'):
        if mode == 'riflemode':
            self.img_object.set_visible(False)
            self.img_riflemode_object.set_visible(True)
            self.rifle_effect.visible(True)
        else:
            self.img_object.set_visible(True)
            self.img_riflemode_object.set_visible(False)
            self.rifle_effect.visible(False)

    def set_pos(self, x, y):
        #The Rifle mode sprite, the Thrust, and also the Beam effect
        #follows the Normal mode Gundam sprite position. 
        self.pos = [x,y]
        self.img_object.set_extent(self.extent())
        self.img_riflemode_object.set_extent(self.extent(mode='riflemode'))
        self.thruster.set_pos(x, y)
        self.rifle_effect.set_pos(x, y)

    def move_right(self, event):
        self.pos[0] += 3
        if not inbound(self.pos):
            self.pos[0] += -3
        self.set_pos(*self.pos)
        self.thruster.move_right()
        self.rifle_effect.set_pos(*self.pos)

    def move_left(self, event):
        self.pos[0] += -3
        if not inbound(self.pos):
            self.pos[0] += 3
        self.set_pos(*self.pos)
        self.thruster.move_left()
        self.rifle_effect.set_pos(*self.pos)

    def move_up(self, event):
        self.pos[1] += 2
        if not inbound(self.pos):
            self.pos[1] += -2
        self.set_pos(*self.pos)
        self.thruster.move_up()
        self.rifle_effect.set_pos(*self.pos)

    def move_down(self, event):
        self.pos[1] += -2
        if not inbound(self.pos):
            self.pos[1] += 2
        self.set_pos(*self.pos)
        self.thruster.move_down()
        self.rifle_effect.set_pos(*self.pos)

    def beam_rifle(self, event):
        self.visible(mode='riflemode')
        

class Thruster(object):
    def __init__(self, ax, pos):
        self.ax = ax
        self.fig = self.ax.figure
        self.pos = pos
        self.state = 'up'
        self.anim_count = 0

        self.img_matrix = {'up': plt.imread('thrust_up.png'), 'down': plt.imread('thrust_down.png'), \
                           'right': plt.imread('thrust_right.png'), 'left': plt.imread('thrust_left.png')}
        self.img_object = {'up': ax.imshow(self.img_matrix['up'], visible = True), 'down': ax.imshow(self.img_matrix['down'], visible=False), \
                           'right': ax.imshow(self.img_matrix['right'], visible = False), 'left': ax.imshow(self.img_matrix['left'], visible =False)}
        
        #calculate dimension:
        self.dim = {} 
        for img in self.img_object.values():
            default_extent = adjust_extent(img.get_extent())
            self.dim[img] = default_extent[1]-default_extent[0], default_extent[3]-default_extent[2]
            img.set_extent(self.extent(img))
        ## 

    def visible(self, direction):
        for key in self.img_object.keys():
            if key == direction:
                self.img_object[key].set_visible(True)
            else:
                self.img_object[key].set_visible(False)
        
    def extent(self, img):
        return [self.pos[0]-self.dim[img][0]/2, self.pos[0]+self.dim[img][0]/2, \
                self.pos[1]-self.dim[img][1]/2, self.pos[1]+self.dim[img][1]/2]

    def set_pos(self, x, y):
        if self.state in ('up', 'right'):
            self.pos = [x-10,y-5]
        if self.state == 'left':
            self.pos = [x+4, y]
        if self.state == 'down':
            self.pos = [x-10, y]
        for img in self.img_object.values():
            img.set_extent(self.extent(img))

    def move_right(self):
        self.visible('right')
        self.anim_count = 0
        self.state = 'right'
        
    def move_left(self):
        self.visible('left')
        self.anim_count = 0
        self.state = 'left'

    def move_up(self):
        self.visible('up')
        self.anim_count = 0
        self.state = 'up'

    def move_down(self):
        self.visible('down')
        self.anim_count = 0
        self.state = 'down'

        
class RifleEffect(object):
    def __init__(self, ax, pos):
        self.ax = ax
        self.fig = self.ax.figure
        self.pos = pos
        self.anim_count = 0

        self.img_matrix = plt.imread('explosion_beam_long.png')
        self.img_object = ax.imshow(self.img_matrix, visible=False)
        
        #calculate dimension:
        default_extent = adjust_extent(self.img_object.get_extent())
        self.dim = default_extent[1]-default_extent[0], default_extent[3]-default_extent[2]
        self.img_object.set_extent(self.extent)
        ##

    def visible(self, boolean):
        self.img_object.set_visible(boolean)

    @property
    def extent(self):
        return [self.pos[0]-self.dim[0]/2, self.pos[0]+self.dim[0]/2, \
                self.pos[1]-self.dim[1]/2, self.pos[1]+self.dim[1]/2]

    def set_pos(self, x, y):
        self.pos = [x+370, y-10]
        self.img_object.set_extent(self.extent)


dt = 0.2
times = [0 + dt*i for i in range(1000)]

fig, ax = plt.subplots()
ax.axis('off')
ax.set_xlim([0, 200])
ax.set_ylim([0, 200])

mat = plt.imread("sky_bg_small.png")
ax.imshow(mat)

fname = "ms_08_normal.png"
fname_rifle = "ms_08_aim.png"
gundam = Gundam(fname, fname_rifle, ax, [100,100])

#creating the Button(s) GUI
ax_right = fig.add_axes([0.9, 0.5, 0.05, 0.075])
btn_right = Button(ax_right, '>')
btn_right.on_clicked(gundam.move_right)

ax_left = fig.add_axes([0.9 - 0.05, 0.5, 0.05, 0.075])
btn_left = Button(ax_left, '<')
btn_left.on_clicked(gundam.move_left)

ax_up = fig.add_axes([0.9 - 0.1/2, 0.5 + 0.075, 0.1, 0.075])
btn_up = Button(ax_up, 'up')
btn_up.on_clicked(gundam.move_up)

ax_down = fig.add_axes([0.9 - 0.1/2, 0.5 -0.075, 0.1, 0.075])
btn_down = Button(ax_down, 'down')
btn_down.on_clicked(gundam.move_down)

ax_beam_rifle = fig.add_axes([0.9 - 0.15/2, 0.5 -3*0.075, 0.15, 0.075])
btn_beam_rifle = Button(ax_beam_rifle, 'beam rifle')
btn_beam_rifle.on_clicked(gundam.beam_rifle)
##

animation = FuncAnimation(fig, animate, frames = times, repeat=True, interval = 50)
plt.show()
