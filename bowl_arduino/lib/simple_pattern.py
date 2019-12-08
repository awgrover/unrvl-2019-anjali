import time
class SimplePattern(object):
    def __init__(self, ring, brightness=0.3):
        self.ring = ring
        self.brightness = brightness
        self.energy = brightness
        self.last_cycle = 0
        self.change_speed = 0.05
        self.timeout = 2.0
        self.last_update = 0
        self.last_dying = 0

        self.position = 0
        self.speed = 0

    def update(self, which, speed):
        now = time.monotonic()

        if which == -1:
            # no change, so continue/die


            if self.is_dying(now):
                # dying
                if self.energy > 0:
                    # only update the energy if we are >0
                    #print("TO %s %s = %s" % (self.last_update, now, now-self.last_update))
                    # print("die %s" % pattern_energy) #self.ring[0] = (255,255,0)
                    if now-self.last_dying > 0.01:
                        self.energy -= 0.01 # FIXME: should be a rate...
                        self.ring.brightness = self.energy
                        self.ring.show() # independant 
                        self.last_dying = now
                        if self.energy <=0:
                            print("  died")

        else:
            # new which/speed
            print("UPD %s %s" % (which, speed))
            self.ring.brightness = self.brightness
            self.energy = self.brightness
            self.speed = speed/1000.0
            self.position = which
            self.last_update = now

        # continue
        self.follow(now)

    def follow(self, now):
        if now - self.last_cycle > self.speed:
            self.ring.fill((0,0,0))
            self.position = (self.position + 1) % len(self.ring)
            if self.energy > 0:
                # print("  %s %s" % (self.position, self.energy))
                pass
            self.ring[ self.position ] = (255,255,0)
            self.last_cycle = now

            self.ring.show()
            self.last_cycle = now

    def is_dying(self, now=time.monotonic()):
        return now - self.last_update > self.timeout
