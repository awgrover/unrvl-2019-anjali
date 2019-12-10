
# six hall-effects around the rim of the bowl.
# we're looking for the hall-effect sensors to trigger, indicating movement around the rim.
# we want a light pattern to "follow" the movement (the sensors).
# and, we need to tell the processing side that movement is happening (send a '*' on each)
# We need timeout (movement stopped).

import board
import neopixel
import time
import digitalio
from exponential_smooth import ExponentialSmooth
from simple_pattern import SimplePattern

# NeoPixel Ring
RingPixelCount = 24
ring = neopixel.NeoPixel(board.D5, RingPixelCount, brightness=0.2, auto_write=False)

# keepint track of "touches"
touch_timout = 2.0 # sec
last_touch = 0
xspeed = ExponentialSmooth(3,0)

# pattern
pattern = SimplePattern(ring)

from adafruit_debouncer import Debouncer
# touch_pins = ( digitalio.DigitalInOut(p) for p in ( board.A1, board.A2, board.A3, board.A4, board.A5, board.D7, board.D9, board.D10))
touch_pins = list( digitalio.DigitalInOut(p) for p in ( board.D11, board.D10, board.D9, board.A5) )
touches = list( Debouncer( pin ) for pin in touch_pins )

def check_for_hall_effect():
    """return the i'th thing touched, and the current speed in msec/touch"""
    global last_touch, xspeed
    saw = -1
    now = time.monotonic()

    for i,a_touch in enumerate(touches):
        a_touch.update()

        if a_touch.fell:
            saw = i
            print("Fall %s" % i)
            if last_touch == 0:
                xspeed.reset(0)
            else:
                xspeed.update( 1000* (now - last_touch ) )

            last_touch = now

    if saw != -1:
        print("speed %s" % xspeed.value)
        return(saw, xspeed.value)
    
    else:
        if pattern.is_dying:
            xspeed.reset(0) # so average doesn't build up
        return(-1, xspeed.value)

# SETUP
for apin in touch_pins:
    apin.direction = digitalio.Direction.INPUT
    # external pull, so "no-detect" is TRUE, "detect" is FALSE

while(True):
    which, speed = check_for_hall_effect()

    if (which == -1 ):
        pattern.update( -1, 0 ) # will fade out
    
    else:
        # when we see a hall-effect

        # signal to processing
        print('*')

        pattern.update( which, speed )

print("EXIT")
