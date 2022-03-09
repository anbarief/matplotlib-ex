import random
import math
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib.animation import FuncAnimation

fanim = FuncAnimation
fig, ax = plt.subplots()

ethan_pos = [-30, 80]
start_poke = [40, 85] 
pokeball_pos = [40, 85]
start_poke2 = [40, 65] 
pokeball_pos2 = [40, 65]
start_poke3 = [40, 45] 
pokeball_pos3 = [40, 45]
start_poke4 = [40, 25] 
pokeball_pos4 = [40, 25]
start_poke5 = [40, 5] 
pokeball_pos5 = [40, 5]
start_poke6 = [40, -15] 
pokeball_pos6 = [40, -15]


def image(file, x_pos = 0, y_pos = 0, size = 1, centerize=True, flip_horizontal=False):
    img = plt.imread(file)
    img = plt.imshow(img)
    extent = img.get_extent()
    extent = [(extent[0]+0.5)*size, extent[1]*size, extent[3]*size, extent[2]*size]
    dim = [extent[1]-extent[0], extent[3]-extent[2]]
    if centerize:
        extent = [extent[0] + x_pos - dim[0]/2, extent[1] + x_pos - dim[0]/2, \
                  extent[2] + y_pos - dim[1]/2, extent[3] + y_pos - dim[1]/2]
    else:
        extent = [extent[0] + x_pos, extent[1] + x_pos, \
                  extent[2] + y_pos, extent[3] + y_pos]

    if flip_horizontal:
        extent = [extent[1], extent[0], \
                  extent[2], extent[3]]
        
    img.set_extent(extent)

def flamethrower(ax, start_pos, end_pos, y, start_frame, end_frame, end_anim, frame):
    N = int((end_frame - start_frame))
    dx = (end_pos - start_pos)/N
    interval = [start_pos + i*dx for i in range(N+1)]
    if start_frame <= frame <= end_anim:
        if frame <= end_frame:
            pass
        else:
            frame = end_frame
        for i in interval[0:(1+frame-start_frame)]:
            for j in range(20):
                ax.plot(i, y+random.gauss(0, 0.01 + 2*i/end_pos), marker = 'o', color=(1, 0.7-(0.7)*i/end_pos,0,1), ms=4)
                ax.plot(i+1/3, y+random.gauss(0, 0.01 + 2*i/end_pos), marker = 'o', color=(1, 0.7-(0.7)*i/end_pos,0,1), ms=4)
                ax.plot(i+2/3, y+random.gauss(0, 0.01 + 2*i/end_pos), marker = 'o', color=(1, 0.7-(0.7)*i/end_pos,0,1), ms=4)
            

def anim(frame):
    ax.cla()

    ax.spines['bottom'].set_color((0,0,0,1))
    ax.spines['top'].set_color((0,0,0,1)) 
    ax.spines['right'].set_color((0,0,0,1))
    ax.spines['left'].set_color((0,0,0,1))
    ax.axis('scaled')
    ax.set_xlim([-20,120]); ax.set_ylim([-50,100])
    ax.tick_params(colors=(0,0,0,0))

    if -20<=frame <= 25:
        ethan_pos[0] = -30 + 55*(frame+20)/45
    
        if frame%3 == 0:
            image('sprites//ethan_right_stand.png', *ethan_pos, 1)
        elif frame%3==1:
            image('sprites//ethan_right_right.png', *ethan_pos, 1)
        else:
            image('sprites//ethan_right_left.png', *ethan_pos, 1)

    if 25 < frame < 40:
        image('sprites//ethan_right_stand.png', *ethan_pos, 1)


    if 40 <= frame <= 50:
        pokeball_pos[0] = start_poke[0] + (frame - start_poke[0])
        pokeball_pos[1] = start_poke[1] -(0.1325)*((frame - start_poke[0]))**2
        image('sprites//pokeball_1.png', *pokeball_pos, 0.02)

    if 40 <= frame < 45:
        image('sprites//ethan_throw.png', *ethan_pos, 1)

    if 45<= frame <=75:
        image('sprites//ethan_right_stand.png', *ethan_pos, 1)

    if 50 <=frame < 55:
        image('sprites//pokeball_1.png', *pokeball_pos, 0.02)

    if 55 <= frame <= 60:
        image('sprites//pokeball_2.png', *pokeball_pos, 0.02)
        image('sprites//smoke_1.png', pokeball_pos[0]+2, pokeball_pos[1], 0.5) 
        image('sprites//charmeleon_left_1.png', pokeball_pos[0] + 1 + 9*(frame-55)/5, 70, 1*(1/5)*(frame-55), centerize=False)

    if 60 < frame <= 75:
        image('sprites//pokeball_2.png', *pokeball_pos, 0.02)
        image('sprites//charmeleon_left_1.png', 60, 70, 1, centerize=False)

    if 75 < frame <= 100:
        char_pos_y = (1+0.025*math.sin(1*(frame-66)))*70 
        image('sprites//ethan_right_stand.png', *ethan_pos, 1)
        image('sprites//pokeball_2.png', *pokeball_pos, 0.02)
        image('sprites//charmeleon_left_1.png', 60, char_pos_y, 1, centerize=False)

    #charmeleon in position
    if 100 < frame <= 700:
        char_pos_y = (1+0.025*math.sin(1*(frame-66)))*70 
        image('sprites//pokeball_2.png', *pokeball_pos, 0.02)
        image('sprites//charmeleon_left_1.png', 60, char_pos_y, 1, centerize=False)


    #ethan walks down
    if 100 < frame <= 120:
        image('sprites//ethan_front.png', *ethan_pos, 1)

    if 120 < frame <= 130:
        ethan_pos[1] = ethan_pos[1] - 20/(130-120)
    
        if frame%3 == 0:
            image('sprites//ethan_front.png', *ethan_pos, 1)
        elif frame%3==1:
            image('sprites//ethan_front_right.png', *ethan_pos, 1)
        else:
            image('sprites//ethan_front_left.png', *ethan_pos, 1)

    #call pokemon
    if 130 < frame <=145 :
        image('sprites//ethan_right_stand.png', *ethan_pos, 1)


    if 145 < frame <= 155:
        pokeball_pos2[0] = start_poke2[0] + (frame - (145))
        pokeball_pos2[1] = start_poke2[1] -(0.1325)*((frame - 145))**2
        image('sprites//pokeball_1.png', *pokeball_pos2, 0.02)


    if 145 < frame <= 150:
        image('sprites//ethan_throw.png', *ethan_pos, 1)

    if 150< frame <=175:
        image('sprites//ethan_right_stand.png', *ethan_pos, 1)

    if 150 < frame <= 155:
        image('sprites//pokeball_1.png', *pokeball_pos2, 0.02)

    if 155 < frame <= 160:
        image('sprites//pokeball_2.png', *pokeball_pos2, 0.02)
        image('sprites//smoke_1.png', pokeball_pos2[0]+2, pokeball_pos2[1], 0.5) 
        image('sprites//lapras_left_1.png', pokeball_pos2[0] + 1 + 9*(frame-156)/4, 50, 1*(1/5)*(frame-155), centerize=False)


    if 160 < frame <= 175:
        image('sprites//pokeball_2.png', *pokeball_pos2, 0.02)
        image('sprites//lapras_left_1.png', 60, 50, 1, centerize=False)

    if 175 < frame <= 200:
        lapras_pos_y = (1+0.025*math.sin(1*(frame-175)))*50 
        image('sprites//ethan_right_stand.png', *ethan_pos, 1)
        image('sprites//pokeball_2.png', *pokeball_pos2, 0.02)
        image('sprites//lapras_left_1.png', 60, lapras_pos_y, 1, centerize=False)

    #lapras in position
    if 200 < frame <= 700:
        lapras_pos_y = (1+0.025*math.sin(1*(frame-175)))*50 
        image('sprites//pokeball_2.png', *pokeball_pos2, 0.02)
        image('sprites//lapras_left_1.png', 60, lapras_pos_y, 1, centerize=False)


    #ethan walks down
    if 200 < frame <= 220:
        image('sprites//ethan_front.png', *ethan_pos, 1)

    if 220 < frame <= 230:
        ethan_pos[1] = ethan_pos[1] - 20/(230-220)
    
        if frame%3 == 0:
            image('sprites//ethan_front.png', *ethan_pos, 1)
        elif frame%3==1:
            image('sprites//ethan_front_right.png', *ethan_pos, 1)
        else:
            image('sprites//ethan_front_left.png', *ethan_pos, 1)


    #call pokemon
    if 230 < frame <=245 :
        image('sprites//ethan_right_stand.png', *ethan_pos, 1)


    if 245 < frame <= 255:
        pokeball_pos3[0] = start_poke3[0] + (frame - (245))
        pokeball_pos3[1] = start_poke3[1] -(0.1325)*((frame - 245))**2
        image('sprites//pokeball_1.png', *pokeball_pos3, 0.02)


    if 245 < frame <= 250:
        image('sprites//ethan_throw.png', *ethan_pos, 1)

    if 250< frame <=275:
        image('sprites//ethan_right_stand.png', *ethan_pos, 1)

    if 250 < frame <= 255:
        image('sprites//pokeball_1.png', *pokeball_pos3, 0.02)

    if 255 < frame <= 260:
        image('sprites//pokeball_2.png', *pokeball_pos3, 0.02)
        image('sprites//smoke_1.png', pokeball_pos3[0]+2, pokeball_pos3[1], 0.5) 
        image('sprites//pidgeot_left_1.png', pokeball_pos3[0] + 1 + 9*(frame-256)/4, 30, 1*(1/5)*(frame-255), centerize=False)

    if 260 < frame <= 275:
        image('sprites//pokeball_2.png', *pokeball_pos3, 0.02)
        pidgeot_pos_y = (1+0.025*math.sin(1*(frame-260)))*30 
        if (frame%6 == 1) or (frame%6 == 2) or (frame%6 == 3):
            image('sprites//pidgeot_left_1.png', 60, pidgeot_pos_y, 1, centerize = False)
        else:
            image('sprites//pidgeot_left_2.png', 60, pidgeot_pos_y, 1, centerize = False)

    if 275 < frame <= 300:
        pidgeot_pos_y = (1+0.025*math.sin(1*(frame-275)))*30 
        image('sprites//ethan_right_stand.png', *ethan_pos, 1)
        image('sprites//pokeball_2.png', *pokeball_pos3, 0.02)
        if (frame%6 == 1) or (frame%6 == 2) or (frame%6 == 3):
            image('sprites//pidgeot_left_1.png', 60, pidgeot_pos_y, 1, centerize = False)
        else:
            image('sprites//pidgeot_left_2.png', 60, pidgeot_pos_y, 1, centerize = False)

    #pidgeot in position
    if 300 < frame <= 700:
        pidgeot_pos_y = (1+0.025*math.sin(1*(frame-300)))*30 
        image('sprites//pokeball_2.png', *pokeball_pos3, 0.02)
        if (frame%6 == 1) or (frame%6 == 2) or (frame%6 == 3):
            image('sprites//pidgeot_left_1.png', 60, pidgeot_pos_y, 1, centerize = False)
        else:
            image('sprites//pidgeot_left_2.png', 60, pidgeot_pos_y, 1, centerize = False)

    #ethan walks down
    if 300 < frame <= 320:
        image('sprites//ethan_front.png', *ethan_pos, 1)

    if 320 < frame <= 330:
        ethan_pos[1] = ethan_pos[1] - 20/(330-320)
    
        if frame%3 == 0:
            image('sprites//ethan_front.png', *ethan_pos, 1)
        elif frame%3==1:
            image('sprites//ethan_front_right.png', *ethan_pos, 1)
        else:
            image('sprites//ethan_front_left.png', *ethan_pos, 1)


    #call pokemon
    if 330 < frame <=345 :
        image('sprites//ethan_right_stand.png', *ethan_pos, 1)

    if 345 < frame <= 355:
        pokeball_pos4[0] = start_poke4[0] + (frame - (345))
        pokeball_pos4[1] = start_poke4[1] -(0.1325)*((frame - 345))**2
        image('sprites//pokeball_1.png', *pokeball_pos4, 0.02)

    if 345 < frame <= 350:
        image('sprites//ethan_throw.png', *ethan_pos, 1)

    if 350< frame <=375:
        image('sprites//ethan_right_stand.png', *ethan_pos, 1)

    if 350 < frame <= 355:
        image('sprites//pokeball_1.png', *pokeball_pos4, 0.02)

    if 355 < frame <= 360:
        image('sprites//pokeball_2.png', *pokeball_pos4, 0.02)
        image('sprites//smoke_1.png', pokeball_pos4[0]+2, pokeball_pos4[1], 0.5) 
        image('sprites//evee_left_1.png', pokeball_pos4[0] + 1 + 9*(frame-356)/4, 10, 1*(1/5)*(frame-355), centerize=False)

    if 360 < frame <= 375:
        image('sprites//pokeball_2.png', *pokeball_pos4, 0.02)
        image('sprites//evee_left_1.png', 60, 10, 1, centerize=False)

    if 375 < frame <= 400:
        evee_pos_y = 10 + (0.025*math.sin(1*(frame-375)))*10 
        image('sprites//ethan_right_stand.png', *ethan_pos, 1)
        image('sprites//pokeball_2.png', *pokeball_pos4, 0.02)
        image('sprites//evee_left_1.png', 60, evee_pos_y, 1, centerize=False)

    #evee in position
    if 400 < frame <= 700:
        evee_pos_y = 10 + (0.025*math.sin(1*(frame-375)))*10  
        image('sprites//pokeball_2.png', *pokeball_pos4, 0.02)
        image('sprites//evee_left_1.png', 60, evee_pos_y, 1, centerize=False)


    #ethan walks down
    if 400 < frame <= 420:
        image('sprites//ethan_front.png', *ethan_pos, 1)

    if 420 < frame <= 430:
        ethan_pos[1] = ethan_pos[1] - 20/(430-420)
    
        if frame%3 == 0:
            image('sprites//ethan_front.png', *ethan_pos, 1)
        elif frame%3==1:
            image('sprites//ethan_front_right.png', *ethan_pos, 1)
        else:
            image('sprites//ethan_front_left.png', *ethan_pos, 1)


    #call pokemon
    if 430 < frame <=445 :
        image('sprites//ethan_right_stand.png', *ethan_pos, 1)

    if 445 < frame <= 455:
        pokeball_pos5[0] = start_poke5[0] + (frame - (445))
        pokeball_pos5[1] = start_poke5[1] -(0.1325)*((frame - 445))**2
        image('sprites//pokeball_1.png', *pokeball_pos5, 0.02)

    if 445 < frame <= 450:
        image('sprites//ethan_throw.png', *ethan_pos, 1)

    if 450< frame <=475:
        image('sprites//ethan_right_stand.png', *ethan_pos, 1)

    if 450 < frame <= 455:
        image('sprites//pokeball_1.png', *pokeball_pos5, 0.02)

    if 455 < frame <= 460:
        image('sprites//pokeball_2.png', *pokeball_pos5, 0.02)
        image('sprites//smoke_1.png', pokeball_pos5[0]+2, pokeball_pos5[1], 0.5) 
        image('sprites//scyther_left_1.png', pokeball_pos5[0] + 1 + 9*(frame-456)/4, -10, 1*(1/5)*(frame-455), centerize=False)

    if 460 < frame <= 475:
        image('sprites//pokeball_2.png', *pokeball_pos5, 0.02)
        image('sprites//scyther_left_1.png', 60, -10, 1, centerize=False)

    if 475 < frame <= 500:
        scyther_pos_y = -10 + (0.025*math.sin(1*(frame-475)))*10 
        image('sprites//ethan_right_stand.png', *ethan_pos, 1)
        image('sprites//pokeball_2.png', *pokeball_pos5, 0.02)
        image('sprites//scyther_left_1.png', 60, scyther_pos_y, 1, centerize=False)

    #scyther in position
    if 500 < frame <= 700:
        scyther_pos_y = -10 + (0.025*math.sin(1*(frame-375)))*10  
        image('sprites//pokeball_2.png', *pokeball_pos5, 0.02)
        image('sprites//scyther_left_1.png', 60, scyther_pos_y, 1, centerize=False)


    #ethan walks down
    if 500 < frame <= 520:
        image('sprites//ethan_front.png', *ethan_pos, 1)

    if 520 < frame <= 530:
        ethan_pos[1] = ethan_pos[1] - 20/(530-520)
    
        if frame%3 == 0:
            image('sprites//ethan_front.png', *ethan_pos, 1)
        elif frame%3==1:
            image('sprites//ethan_front_right.png', *ethan_pos, 1)
        else:
            image('sprites//ethan_front_left.png', *ethan_pos, 1)


    #call pokemon
    if 530 < frame <=545 :
        image('sprites//ethan_right_stand.png', *ethan_pos, 1)

    if 545 < frame <= 555:
        pokeball_pos6[0] = start_poke6[0] + (frame - (545))
        pokeball_pos6[1] = start_poke6[1] -(0.1325)*((frame - 545))**2
        image('sprites//pokeball_1.png', *pokeball_pos6, 0.02)

    if 545 < frame <= 550:
        image('sprites//ethan_throw.png', *ethan_pos, 1)

    if 550< frame <=575:
        image('sprites//ethan_right_stand.png', *ethan_pos, 1)

    if 550 < frame <= 555:
        image('sprites//pokeball_1.png', *pokeball_pos6, 0.02)

    if 555 < frame <= 560:
        image('sprites//pokeball_2.png', *pokeball_pos6, 0.02)
        image('sprites//smoke_1.png', pokeball_pos6[0]+2, pokeball_pos6[1], 0.5) 
        image('sprites//totodile_left_1.png', pokeball_pos6[0] + 1 + 9*(frame-556)/4, -30, 1*(1/5)*(frame-555), centerize=False)

    if 560 < frame <= 575:
        image('sprites//pokeball_2.png', *pokeball_pos6, 0.02)
        image('sprites//totodile_left_1.png', 60, -30, 1, centerize=False)

    if 575 < frame <= 600:
        totodile_pos_y = -30 + (0.025*math.sin(1*(frame-575)))*30 
        image('sprites//ethan_right_stand.png', *ethan_pos, 1)
        image('sprites//pokeball_2.png', *pokeball_pos6, 0.02)
        image('sprites//totodile_left_1.png', 60, totodile_pos_y, 1, centerize=False)

    #totodile in position
    if 600 < frame <= 700:
        totodile_pos_y = -30 + (0.025*math.sin(1*(frame-575)))*30  
        image('sprites//pokeball_2.png', *pokeball_pos6, 0.02)
        image('sprites//totodile_left_1.png', 60, totodile_pos_y, 1, centerize=False)

    #ethan in position
    if 600 < frame <= 700:
        image('sprites//ethan_right_stand.png', 25, -20, 1)


    if 750 < frame <= 1000:
        ax.set_xlim([0, 110]); ax.set_ylim([0, 100])
        pidgeot_pos_y = (1+0.025*math.sin(1*(frame-750)))*70
        if (frame%4 == 1) or (frame%4 == 2):
            image('sprites//pidgeot_front_1.png', 20, pidgeot_pos_y, 1, centerize = False)
        else:
            image('sprites//pidgeot_front_2.png', 20, pidgeot_pos_y, 1, centerize = False)
        image('sprites//evee_front_1.png', 10, 40, 1, centerize = False)
        image('sprites//scyther_front_1.png', 22, 40, 1, centerize = False)
        image('sprites//lapras_front_1.png', 40, 40, 1, centerize = False)
        image('sprites//charmeleon_front_left.png', 61, 40, 1, centerize = False)
        image('sprites//totodile_front_1.png', 72, 40, 1, centerize = False)

    if 800 <= frame <= 830:
        ethan_pos_x = 120 - 37*(frame-800)/30
        if frame%3 == 0:
            image('sprites//ethan_right_stand.png', ethan_pos_x, 40, 1, centerize = False, flip_horizontal = True)
        elif frame%3==1:
            image('sprites//ethan_right_right.png', ethan_pos_x, 40, 1, centerize = False, flip_horizontal = True)
        else:
            image('sprites//ethan_right_left.png', ethan_pos_x, 40,  1, centerize = False, flip_horizontal = True)

    if 830 < frame:
        image('sprites//ethan_front.png', 83, 40, 1, centerize = False)

    if 850 <= frame < 880:
        if frame < 860:
            number = '3'
            bound = 850
        elif 860 <= frame < 870:
            number = '2'
            bound = 860
        else:
            number = '1'
            bound = 870
        ax.text(55, 20, number, ha='center', va='center', color= (0,0,0,1-((frame-bound)/9)), fontsize=50, fontweight='bold')

animation = fanim(fig, anim, frames = range(-60, 1100), interval = 100)
plt.show()
