from matplotlib import pyplot as plt
from matplotlib.pyplot import draw, pause
import sys
from FeedImage import FeedImage
from Bug import Bug

def update_bug():
    new_loc = bug.get_location()
    bug.eat(image.get_pixel(new_loc))
    image.draw_pixel(new_loc)

def bug_input(event):
    global move_func
    if event.key == "escape":
        sys.exit()
    elif event.key == "r":
        move_func = bug.chase_light
    elif event.key == "a":
        move_func = bug.learn_move
        bug.give_taste(image.get_pixel)
    elif event.key in ("up", "down", "left", "right"):
        move_func = bug.move_directed
        run_bug(event)

    sys.stdout.flush()

def run_bug(event = None):
    image.clear_space(bug.get_location())
    move_func(event)
    update_bug()
    
def onclick(event):
    cx, cy = int(event.xdata), int(event.ydata)
    image.addLights([(cx, cy)])

image = FeedImage(400,400) #Could modify using Blit to update background
fig, ax = plt.subplots()
visual = ax.imshow(image.image, cmap='gist_gray')

bug = Bug(5, 5, 400, 400)
move_func = bug.chase_light
bug.give_sight(image.get_pixel)
update_bug()

cid = fig.canvas.mpl_connect('button_press_event', onclick)
b_press = fig.canvas.mpl_connect('key_press_event', bug_input)

while True:
    run_bug()
    visual.set_data(image.image)
    draw()
    pause(.1)