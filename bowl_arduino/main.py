
# six hall-effects around the rim of the bowl.
# we're looking for the hall-effect sensors to trigger, indicating movement around the rim.
# we want a light pattern to "follow" the movement (the sensors).
# and, we need to tell the processing side that movement is happening (send a '*' on each)
# We need timeout (movement stopped).

import board
import neopixel
import time
from exponential_smooth import ExponentialSmooth
from simple_pattern import SimplePattern

# NeoPixel Ring
RingPixelCount = 10
ring = neopixel.NeoPixel(board.NEOPIXEL, RingPixelCount, brightness=0.2, auto_write=False)

# keepint track of "touches"
touch_timout = 2.0 # sec
last_touch = 0
xspeed = ExponentialSmooth(3,0)

# pattern
pattern = SimplePattern(ring)

# FIXME: fake touch as hall-effect
import touchio
from edge_detect import Edge
touches = list( Edge( touchio.TouchIn( pin )) for pin in ( board.A1, board.A2, board.A3, board.A4, board.A5, board.A6, board.A7) )

def check_for_hall_effect():
    """return the i'th thing touched, and the current speed in msec/touch"""
    global last_touch, xspeed
    saw = -1
    now = time.monotonic()

    for i,a_touch in enumerate(touches):
        a_touch.update()

        if a_touch.rose:
            saw = i
            if last_touch == 0:
                xspeed.reset(0)
            else:
                xspeed.update( 1000* (now - last_touch ) )

            last_touch = now

    if saw != -1:
        print("speed %s" % xspeed.value)
        return(saw, xspeed.value)
    
    else:
        return(-1, xspeed.value)

def update_pattern(which, speed):
    global pattern_energy,pattern_last_cycle,pattern_speed

    now = time.monotonic()

    if speed == 0:
        pattern.dying()

    else:
        print("up %d %d" % (which,speed))
        pattern.follow( (which + 4) % len(touches), speed)

while(True):
    which, speed = check_for_hall_effect()

    if (which == -1 ):
        if time.monotonic() - last_touch > touch_timout:
            update_pattern( -1, 0 ) # will fade out
    
    else:
        # when we see a hall-effect

        # signal to processing
        print('*')

        update_pattern( which, speed )

print("EXIT")
