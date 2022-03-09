#Copyright Arief Anbiya (2020)
#E-mail: anbarief@live.com

##Fourier Sine Series Visualization

import math

from matplotlib.patches import Circle
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


#Making the CircleViz class (an object of this class is associated with 1 sine wave)
class CircleViz:
    def __init__(self, center, wave, point_on_wave=0, parent = None):
        if parent == None:
            self.center = center
        else:
            self.center = [parent.x + parent.r, parent.y + parent.r]
        self.r = wave.amp #the radius follows the wave amplitude
        self.x, self.y = self.center[0], self.center[1]
        self.wave = wave #attaching a SineViz object
        self.wv_point = point_on_wave

        self.circle_patch = Circle(self.center, radius = self.r, color = (0,0,1,0.05), ec = (0,0,1,0.25))
        self.child = None

    def update_pos(self):
        self.x = self.center[0]
        self.y = self.center[1]
        self.circle_patch.center = self.center

    def plot_circle(self, ax):
        ax.add_patch(self.circle_patch)

    def plot_vector(self, ax, theta, draw  = True):
        if draw:
            ax.plot([self.x, self.x + self.r*math.cos(theta)], \
                    [self.y, self.y + self.r*math.sin(theta)], '-', color = 'crimson', lw=3)

            ax.plot(self.x + self.r*math.cos(theta),  self.y + self.r*math.sin(theta), 'o', color = (0,0,1,0.5))

        point = [self.x + self.r*math.cos(theta),  self.y + self.r*math.sin(theta)]

        #updating the center of child circle:
        if (self.child != None):
            self.child.center = point
            self.child.update_pos()
        
        return point

#Making the SineViz class (an object of this class represents 1 sine wave)
class SineViz:
    def __init__(self, amp, omega, velocity, color, phase=0):
        self.amp = amp
        self.omg = omega
        self.c = velocity
        self.color = color
        self.phase = phase

        self.func = lambda x,t: self.amp*math.sin(self.phase + self.omg*(x - self.c*t))

    def plot_wave(self, ax, x_values, t):
        y = [self.func(x, t) for x in x_values]
        ax.plot(x_values, y, '-', color = self.color)


class FourierSeriesViz:
    def __init__(self, waves, bigcircle_x = -10, point_on_wave = 0):
        #the lowest index is wave w/ the highest amplitude
        self.waves = sorted(waves, key = lambda x: abs(x.amp), reverse=True)  

        self.circles = [CircleViz([bigcircle_x,0], self.waves[0], point_on_wave)] #Big circle as first one
        for wave in self.waves[1:]:
            circle = CircleViz([0,0], wave, point_on_wave, parent = self.circles[-1])
            self.circles[-1].child = circle
            self.circles.append(circle)

    def plot(self, ax, x_values, t, draw=True):
        for circle in self.circles:
            if draw:
                circle.plot_circle(ax)
            theta = circle.wave.omg*(circle.wv_point - circle.wave.c*t) + circle.wave.phase
            point = circle.plot_vector(ax, theta, draw) 

        if draw:
            for wave in self.waves:
                wave.plot_wave(ax, x_values, t)

            wave_sum = [  sum([wave.func(x, t) for wave in self.waves]) for x in x_values]
            ax.plot(x_values, wave_sum, '-', lw = 2, color = 'blue')

            wave_sum_yp = sum([wave.func(0, t) for wave in self.waves]) 
            ax.plot([point[0], 0], [point[1], wave_sum_yp], '--', color = (0.2, 0.2, 0.2, 0.5))
            
        return point

fig, ax = plt.subplots()


time_points = [0 + 500*i/40000 for i in range(40001)] 
n_time = len(time_points)

waves = [SineViz(15/((i)*math.pi), i, 3, color = (0,0,0,0.1))  for i in range(1, 30, 2)]
title = ""
x = [0 + 10*math.pi*i/5000 for i in range(5001)]
N=len(waves)
fourier_series = FourierSeriesViz(waves[0:N])
draw_points_x = []
draw_points_y = []

fig.set_facecolor((1, 1, 1, 1))

def animate(frame):
    ax.cla()
    ax.axis('scaled')
    ax.tick_params(colors=(0,0,0,0))
    ax.set_facecolor((1, 1, 1, 0.75))

    color = 'black'
    t = time_points[frame]
    if frame > 0:
        t_prev = time_points[frame-1]
        t_interval = [t_prev + i*(t-t_prev)/300 for  i in range(301)]
        points = [fourier_series.plot(ax, x, i, False) for i in t_interval[0:300]]
        draw_points_x.extend([p[0] for p in points]); draw_points_y.extend([p[1] for p in points])
        point = fourier_series.plot(ax, x, t)
        draw_points_x.append(point[0]); draw_points_y.append(point[1])
        ax.plot(draw_points_x, draw_points_y, '-', color = color, lw = 1)
    else:
        point = fourier_series.plot(ax, x, t)
        draw_points_x.append(point[0]); draw_points_y.append(point[1])
        ax.plot(draw_points_x, draw_points_y, '-', color = color, lw = 1)
        

    ax.set_xlim([-20, 20])
    ax.set_ylim([-10, 10])
    ax.text(-18, 8, r"$t = {}$".format(round(t,3)), color = 'gray', fontsize=15)
    ax.text(-18, 7, r"$N = {}$".format(N), color = 'gray', fontsize=15)
    ax.set_title(title, color = 'gray')

    
animation = FuncAnimation(fig, animate, frames = range(n_time), repeat = False, interval = 100)
plt.show()
