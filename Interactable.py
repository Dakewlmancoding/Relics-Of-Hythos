from Wrappers import Geom

from panda3d.core import CollisionNode, CollisionHandlerEvent


class InteractableFuncs():
    def __init__(self):
        #vars related to the statue
        self.statuePositions = [-60,30,120]
        self.statueIncrimenter = 0
        self.statueLookedAt = []

    # ##Interactable Funcs
    #(NTS: convention is name the function the capitalized name of the interactable)
    
    #what it says on the tin
    def Sound(self, sound):
        sound.play()

    #used for objects that were built as interactables, but later had their functions removed, and it was too time consuming to totally rebuild them as geom
    def Dummy(self):
        print("duhhh... I'm a dummy!")

    def Statue(self, statue, directon):
        print("started at", self.statueIncrimenter)
        if (statue.object.model.getH() == -190) and (self.statueIncrimenter == 0) and (directon == "forwards"):
            self.statueIncrimenter = 0
        elif self.statueIncrimenter == 0:
            if directon == "forwards":
                self.statueIncrimenter +=1
            elif directon == "backwards":
                self.statueIncrimenter = 2
        elif self.statueIncrimenter == 1:
            if directon == "forwards":
                self.statueIncrimenter +=1
            elif directon == "backwards":
                self.statueIncrimenter -= 1
        elif self.statueIncrimenter == 2:
            if directon == "forwards":
                self.statueIncrimenter = 0
            elif directon == "backwards":
                self.statueIncrimenter -= 1

        print("ended at", self.statueIncrimenter)

        if self.statueIncrimenter == 0:
            statue.object.model.setH(self.statuePositions[0])
            self.statueLookedAt.append("blue")
        elif self.statueIncrimenter == 1:
            statue.object.model.setH(self.statuePositions[1])
            self.statueLookedAt.append("green")
        elif self.statueIncrimenter == 2:
            statue.object.model.setH(self.statuePositions[2])
            self.statueLookedAt.append("red")

        print("Statue Rotated")
        print(self.statueLookedAt, "next should be", self.statueIncrimenter)

        if len(self.statueLookedAt) >= 3:
            if self.statueLookedAt == ["blue", "red", "green"]:
                return True
            else:
                self.statueIncrimenter = 0
                statue.object.model.setH(-190)
                self.statueLookedAt = []



class Interactable():
    #note to prof: Functions are first-class objects in Python, so you can pass them in as a parameter, which is what I'm doing here for 'interactFunc'
    def __init__(self, name, path, loader, interactFunc, collisionZone, triggerZone, scale=[1], xPos=0, yPos=0, zPos=0):
        self.xPos = xPos
        self.yPos = yPos
        self.zPos = zPos
        self.interactFunc = interactFunc

        self.object = Geom(path, scale, loader, xPos, yPos, zPos)

        triggerZone.tangible = False
        tColliderNode = CollisionNode(name)
        tColliderNode.addSolid(triggerZone)
        self.tCollider = self.object.model.attachNewNode(tColliderNode)

        cColliderNode = CollisionNode(name+"CZone")
        cColliderNode.addSolid(collisionZone)
        self.cCollider = self.object.model.attachNewNode(cColliderNode)


    #puts the object in the scene. wraps the Geom func of the same name
    def render(self, renderer):
        self.object.render(renderer)
    
    #displays the trigger zone
    def showTZ(self):
        self.tCollider.show()

    #diplays the collision zone
    def showCZ(self):
        self.cCollider.show()
