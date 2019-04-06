import math

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation 
import matplotlib.font_manager as fm

##Setting font properties
file = "image.png"
sophia_regular_otf = "Sofia-Regular.otf"
sophia_regular = fm.FontProperties(fname = sophia_regular_otf, size = 30)
sophia_regular_big = fm.FontProperties(fname = sophia_regular_otf, size = 50)

fig, ax = plt.subplots()

##Adjusting image size/extent
matrix = plt.imread(file)
img = ax.imshow(matrix)
extent = img.get_extent()
new_extent = (extent[0], extent[1], extent[3], extent[2])
width = abs(extent[1] - extent[0])
scaled = (extent[0]*0.5 + width/4, extent[1]*0.5 + width/4, \
          extent[3]*0.5 + 250, extent[2]*0.5 + 250) 
img.set_extent(scaled)

#Adjusting background color, axis limit, and showing text
ax.set_xlim(new_extent[0:2])
ax.set_ylim(new_extent[2:]) 
ax.set_axis_bgcolor((251/255, 236/255, 93/255, 1))
ax.tick_params(colors = (0,0,0,0))
t1 = ax.text(width*0.7, 700, "Soedja", fontproperties = sophia_regular)
t2 = ax.text(0.3*width, 700, "ajdeoS", fontproperties = sophia_regular, ha = 'right')
t3 = ax.text(0.6*width, 100, "Grab it now!", fontproperties = sophia_regular_big, \
             ha = 'center')


def anim_func(frame):
    #animation function, using a periodic function cosine to fluctuate the image position and the text size
    extent = img.get_extent()
    mult = 3*math.cos(10*frame*0.1)
    update_fp = fm.FontProperties(fname = sophia_regular_otf, size = 50 + mult)
    new_extent = (extent[0], extent[1], extent[2] + mult, extent[3] + mult)
    img.set_extent(new_extent)
    t3.set_fontproperties(update_fp)

fanim = FuncAnimation(fig = fig, func = anim_func, interval = 100, repeat = True)
#fanim.save("test.mp4")
