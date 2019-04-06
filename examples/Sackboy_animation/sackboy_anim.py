import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib.animation import FuncAnimation

sophia_regular_otf = "Sofia-Regular.otf"
sophia_regular = fm.FontProperties(fname = sophia_regular_otf, size = 20)

class ChangeColorSackBoy:
    def __init__(self):
        self.fig, self.ax = plt.subplots()
        img_mat = plt.imread("sackboy.png")
        self.img = self.ax.imshow(img_mat)
        self.info = " Click on a node to change it's color."

        extent = self.img.get_extent()
        self.width = abs(extent[0]-extent[1])
        self.height = abs(extent[2]-extent[3])

        new_extent = (extent[0], extent[1], extent[3], extent[2])
        self.img.set_extent(new_extent)

        self.ax.set_xlim([-self.width, 2*self.width])
        self.ax.set_ylim([0, 2*self.height])

        self.text = self.ax.text(0.5*self.width, 1.2*self.height, self.info, \
                                 fontproperties = sophia_regular, ha = "center", va = "center")
        self.text.set_rotation_mode("anchor")

        self.ax.tick_params(colors = (0,0,0,0))

    def show(self):
        self.fig.show()

    def animation(self, frame):
        self.text.set_rotation(math.cos(frame)*20)
        
    def animate(self):
        anim = FuncAnimation(self.fig, self.animation, frames = [i*2*math.pi/200 for i in range(201)], \
                             interval = 1, repeat = True)
        plt.show(block = True)
        return anim

sackboy = ChangeColorSackBoy()
sackboy.animate()
