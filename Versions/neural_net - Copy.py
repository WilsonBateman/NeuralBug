import numpy as np
from FeedImage import FeedImage
from Bug import Bug
from matplotlib.pyplot import subplots,close
from matplotlib import cm

def run_bug():
    while 1 == 1:
        image.clear_bug(bug.get_location())
        bug.move()
        image.draw_bug(bug.get_location())
        yield image.image.load()

def mplrun(niter=1000):
    """ Visualise the simulation using matplotlib, using blit for 
    improved speed"""
    fig,ax = subplots(1,1)
    rw = run_bug()
    im = ax.imshow(rw.next(),interpolation='nearest',cmap=cm.hot,animated=True)
    fig.canvas.draw()
    background = fig.canvas.copy_from_bbox(ax.bbox) # cache the background

    for ii in xrange(niter):
        im.set_data(rw.next())          # update the image data
        fig.canvas.restore_region(background)   # restore background
        ax.draw_artist(im)          # redraw the image
        fig.canvas.blit(ax.bbox)        # redraw the axes rectangle

    close(fig)

bug = Bug(5,5)
image = FeedImage(400,400)
mplrun()


