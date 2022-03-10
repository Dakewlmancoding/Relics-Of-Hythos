
from direct.showbase import DirectObject
from direct.task import Task


# ### EVENT HANDLER ###

#mostly just gets key strokes and updates variables for app to check. I feel like this is inefficient, but as of yet cannot think of a neater way to do this
class Events(DirectObject.DirectObject):
    def __init__(self):
        # ## Internal Vars
        self.e = False
        self.q = False
        self.p = False

        self.w = False
        self.a = False
        self.s = False
        self.d = False
        self.space = False

        self.r = False
        self.f = False
        self.v = False

        self.x = False

        self.inWaterfallBlueZone = False
        self.inWaterfallRedZone = False
        self.inWaterfallGreenZone = False
        self.inDummyZone = False
        self.inStatueZone = False
        self.solved = False

        self.accept('p', self.pPressed)
        self.accept('p-up', self.pDepressed)

        self.accept('e', self.ePressed)
        self.accept('e-up', self.eDepressed)

        self.accept('q', self.qPressed)
        self.accept('q-up', self.qDepressed)

        self.accept('r', self.rPressed)
        self.accept('r-up', self.rDepressed)

        self.accept('w', self.wPressed)
        self.accept('w-up', self.wDepressed)

        self.accept('a', self.aPressed)
        self.accept('a-up', self.aDepressed)

        self.accept('s', self.sPressed)
        self.accept('s-up', self.sDepressed)

        self.accept('d', self.dPressed)
        self.accept('d-up', self.dDepressed)
        
        self.accept('space', self.spacePressed)
        self.accept('space-up', self.spaceDepressed)

        self.accept('f', self.fPressed)
        self.accept('f-up', self.fDepressed)

        self.accept('v', self.vPressed)
        self.accept('v-up', self.vDepressed)

        self.accept('x', self.xPressed)
        self.accept('x-up', self.xDepressed)

        self.accept("player-into-waterfallBlue", self.waterfallBlueEnter)
        self.accept("player-out-waterfallBlue", self.waterfallBlueExit)

        self.accept("player-into-waterfallRed", self.waterfallRedEnter)
        self.accept("player-out-waterfallRed", self.waterfallRedExit)

        self.accept("player-into-waterfallGreen", self.waterfallGreenEnter)
        self.accept("player-out-waterfallGreen", self.waterfallGreenExit)

        self.accept("player-into-dummy", self.dummyEnter)
        self.accept("player-out-dummy", self.dummyExit)

        self.accept("player-into-statue", self.statueEnter)
        self.accept("player-out-statue", self.statueExit)

        self.acceptOnce("solved", self.isSolved)

    # ##Events
    def pPressed(self):
        self.p = True
    def pDepressed(self):
        self.p = False

    def rPressed(self):
        self.r = True
    def rDepressed(self):
        self.r = False

    def fPressed(self):
        self.f = True
    def fDepressed(self):
        self.f = False

    def vPressed(self):
        self.v = True
    def vDepressed(self):
        self.v = False

    def ePressed(self):
        self.e = True
    def eDepressed(self):
        self.e = False

    def qPressed(self):
        self.q = True
    def qDepressed(self):
        self.q = False

    def wPressed(self):
        self.w = True
    def wDepressed(self):
        self.w = False
    
    def aPressed(self):
        self.a = True
    def aDepressed(self):
        self.a = False
    
    def sPressed(self):
        self.s = True
    def sDepressed(self):
        self.s = False
    
    def dPressed(self):
        self.d = True
    def dDepressed(self):
        self.d = False

    def spacePressed(self):
        self.space = True
    def spaceDepressed(self):
        self.space = False

    def xPressed(self):
        self.x = True
    def xDepressed(self):
        self.x = False

    def waterfallBlueEnter(self, entry):
        self.inWaterfallBlueZone = True
        print(entry)
    def waterfallBlueExit(self, entry):
        self.inWaterfallBlueZone = False
        print(entry)
    
    def waterfallRedEnter(self, entry):
        self.inWaterfallRedZone = True
        print(entry)
    def waterfallRedExit(self, entry):
        self.inWaterfallRedZone = False
        print(entry)
    
    def waterfallGreenEnter(self, entry):
        self.inWaterfallGreenZone = True
        print(entry)
    def waterfallGreenExit(self, entry):
        self.inWaterfallGreenZone = False
        print(entry)

    def dummyEnter(self, entry):
        self.inDummyZone = True
        print(entry)
    def dummyExit(self, entry):
        self.inDummyZone = False
        print(entry)

    def statueEnter(self, entry):
        self.inStatueZone = True
        print(entry)
    def statueExit(self, entry):
        self.inStatueZone = False
        print(entry)

    def isSolved(self):
        self.solved = True