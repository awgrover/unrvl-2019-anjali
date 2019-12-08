"""
`edge_detect
====================================================

Given a pin or lambda, detects changes: raise, fall (preds), state (current)
"""

# imports

__version__ = "0.0"

import time
from micropython import const

class Edge(object):
    """Edge detect"""

    def __init__(self, anobject):
        """Make am instance.
           :param object w/.value: uses the .value
        """
        # states are -1,0,1
        self.state = 0x00
        self.was_state = 0x00
        self.changed = False
        self.anobject = anobject

    def update(self):
        """Update the state. MUST be called frequently"""
        self.state = self.anobject.value # should work with t|f, 1|0, etc
        #print("  %s" % self.state);

        if self.state != self.was_state:
            self.changed = True
            self.was_state = self.state
            # print("changed =%s" % (self.state) )

        return self.state # convenient

    @property
    def value(self):
        """Return the current debounced value."""
        return self.state


    @property
    def rose(self):
        """Return whether the debounced value went from low to high at the most recent update."""
        if self.changed:
            self.changed = False
            return self.state # FIXME: only works with t|f .value



    @property
    def fell(self):
        """Return whether the debounced value went from high to low at the most recent update."""
        if self.changed:
            self.changed = False
            return not self.state # FIXME: only works with t|f .value
