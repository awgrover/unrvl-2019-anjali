import time
class SimplePattern(object):
    def __init__(self, ring, brightness=0.3):
        self.ring = ring
        self.brightness = brightness
        self.energy = brightness
        self.last_cycle = 0
        self.change_speed = 0.05
        self.last_pixel = 0

    def dying(self):
        """Continue dying"""
        now = time.monotonic()

        if self.energy > 0 and now - self.last_cycle > self.change_speed:
            # print("die %s" % pattern_energy)
            #self.ring[0] = (255,255,0)
            self.energy -= 0.01 # FIXME: should be a rate...
            self.ring.brightness = self.energy
            self.last_cycle = now
            self.ring.show()

    def follow(self, which, speed):
        self.last_cycle = time.monotonic()
        self.energy = self.ring.brightness

        self.ring.fill((0,0,0))
        self.ring[ which ] = (255,255,0)
        self.ring.brightness = self.brightness
        self.ring.show()


