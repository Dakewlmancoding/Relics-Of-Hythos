# ###IMPORTS###
import imp
from math import *

from Events import Events
from Wrappers import *
from Interactable import Interactable, InteractableFuncs

from direct.showbase import DirectObject
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import Sequence
from panda3d.core import BitMask32
from panda3d.core import DirectionalLight, AmbientLight
from panda3d.core import Point3, CollisionNode, CollisionSphere, CollisionInvSphere, CollisionCapsule, CollisionBox, CollisionTraverser, CollisionHandlerGravity, CollisionHandlerPusher, CollisionHandlerEvent, CollisionHandlerQueue

# ###VAR DECL###
events = Events()
iFuncs = InteractableFuncs()

# ###SETUP###
class MyApp(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)
        self.messenger = messenger

        # ##internal Vars
        mask = BitMask32.bit( 1 )

        # ##Collision setup
        self.cTrav = CollisionTraverser()
        self.pusher = CollisionHandlerPusher()
        self.pusher.setHorizontal(True)
        self.pusher.addInPattern("%fn-into-%in")
        self.pusher.addOutPattern("%fn-out-%in")

        


        # ##Level Geometry

        # #Lights
        ambientLight = AmbientLight('ambientLight')
        ambientLight.setColor((1, 1, 1, 1))
        ambientLightNP = render.attachNewNode(ambientLight)
        render.setLight(ambientLightNP)




        # #Cave
        cave = Geom("models/cave.bam", [.6], self.loader)
        caveColliderNode = CollisionNode("caveSphere")
        caveSphere = caveColliderNode.addSolid(CollisionInvSphere(0,0,0,18))
        caveSphereCollider = cave.model.attachNewNode(caveColliderNode)
        cave.render(self.render)

        # #Statue
        statueColZone = CollisionCapsule(0,0,100,0,0,-100,30)
        statueTZone = CollisionCapsule(0,0,100,0,0,-100,70)
        self.statue = Interactable("statue", "models/interactables/statue.bam", self.loader, iFuncs.Statue, statueColZone, statueTZone,[.025])
        self.statue.object.model.setH(-190)
        self.statue.render(self.render)
        #self.statue.showTZ()

        # #waterfalls
        waterfallBlueColZone = CollisionBox(Point3(5, 0, 0),17,8,20)
        waterfallBlueTZone = CollisionBox(Point3(5, 0, 0),17,15,20)
        self.waterfallBlue = Interactable("waterfallBlue", "models/interactables/waterFallBlue.bam", self.loader, iFuncs.Sound, waterfallBlueColZone, waterfallBlueTZone,[.15])
        self.waterfallBlue.render(self.render)
        self.waterfallBlue.object.model.setH(120)
        self.waterfallBlue.object.model.setPos(-7,-5.5,-.25)
        self.waterfallBlueSound = self.loader.loadSfx("sounds/Blue.mp3")

        waterfallRedColZone = CollisionBox(Point3(5, 0, 0),17,8,20)
        waterfallRedTZone = CollisionBox(Point3(5, 0, 0),17,15,20)
        self.waterfallRed = Interactable("waterfallRed", "models/interactables/waterFallRed.bam", self.loader, iFuncs.Sound, waterfallRedColZone, waterfallRedTZone,[.15])
        self.waterfallRed.render(self.render)
        self.waterfallRed.object.model.setH(-60)
        self.waterfallRed.object.model.setPos(7,5.5,-.25)
        #self.waterfallRed.showTZ()
        self.waterfallRedSound = self.loader.loadSfx("sounds/Red.mp3")

        
        waterfallGreenColZone = CollisionBox(Point3(5, 0, 0),17,8,20)
        waterfallGreenTZone = CollisionBox(Point3(5, 0, 0),17,15,20)
        self.waterfallGreen = Interactable("waterfallGreen", "models/interactables/waterFallGreen.bam", self.loader, iFuncs.Sound, waterfallGreenColZone, waterfallGreenTZone,[.15])
        self.waterfallGreen.render(self.render)
        self.waterfallGreen.object.model.setH(210)
        self.waterfallGreen.object.model.setPos(6,-8,-.25)
        #self.waterfallGreen.showTZ()
        self.waterfallGreenSound = self.loader.loadSfx("sounds/Green.mp3")

        dummyColZone = CollisionBox(Point3(0, 0, 0),0.1,0.1,0.1)
        dummyTZone = CollisionBox(Point3(0,0,0),500,500,500)
        self.dummy = Interactable("dummy", "models/interactables/waterFallGreen.bam", self.loader, iFuncs.Sound, dummyColZone, dummyTZone,[.0015])
        self.dummy.render(self.render)
        self.dummy.object.model.setPos(1,8,0)
        #self.dummy.showTZ()
        self.dummySound = self.loader.loadSfx("sounds/full.mp3")
        


        # ##Player##
        #add a animated/moving model to the scene
        playerAnims = {"walk": "models/player/walk.bam", "idle": "models/player/idle.bam", "dance":"models/player/dance.bam"}
        self.playerActor = Actor("models/player/player.bam", playerAnims)
        self.playerActor.setScale(1,1,1)
        self.playerActor.setPos(-4,5,0)
        self.playerActor.reparentTo(self.render)

        playerColliderNode = CollisionNode("player")
        playerColliderNode.addSolid(CollisionCapsule(0,0,.6,0,0,.4,.3))
        playerCollider = self.playerActor.attachNewNode(playerColliderNode)
        #playerCollider.show()

        self.pusher.addCollider(playerCollider, self.playerActor)
        self.cTrav.addCollider(playerCollider, self.pusher)

        # #Camera
        self.cameraPitch = -15
        self.cameraHeight = 2
        self.camera.reparentTo(self.playerActor)
        self.updateCamera()

        cameraColliderNode = CollisionNode("camera")
        cameraColliderNode.addSolid(CollisionSphere(0,0,0,1))
        cameraCollider = self.camera.attachNewNode(cameraColliderNode)
        self.pusher.addCollider(cameraCollider, self.camera)
        self.cTrav.addCollider(cameraCollider, self.pusher)
        self.disableMouse()



        #gravity stuff ###NYI###
        self.gravity = CollisionHandlerGravity()
        self.gravity.addCollider(playerCollider, self.playerActor)
        self.gravity.setMaxVelocity(15)
        self.gravity.setGravity(9.81)


        # Tasks
        self.taskMgr.add(self.update, "update")

    # ##Task Funcs
    #Note to prof: update here is the equivelent of 'Draw'
    def update(self, task):
        if events.e:
            self.rotate('e')
        if events.q:
            self.rotate('q')

        if events.r:
            self.cameraPitch += .5
            if (self.cameraHeight - .05) <= .8:
                self.cameraHeight = .81
            else:
                self.cameraHeight -= .05
        if events.f:
            self.cameraPitch -= .5
            self.cameraHeight += .05
        if events.v:
            self.cameraPitch = -15
            self.cameraHeight = 2
        self.updateCamera()
        
        if events.solved:
            self.startAnim("dance")
        elif events.w or events.a or events.s or events.d:
            self.startAnim("walk")
        else:
            self.startAnim("idle")

        if events.w:
            self.move('w')
        if events.a:
            self.move('a')
        if events.s:
            self.move('s')
        if events.d:
            self.move('d')
        if events.space:
            self.move(' ')
        
        if events.p:
            self.debug()

        if events.x:
            if events.inWaterfallBlueZone:
                self.waterfallBlue.interactFunc(self.waterfallBlueSound)
            if events.inWaterfallRedZone:
                self.waterfallRed.interactFunc(self.waterfallRedSound)
            if events.inWaterfallGreenZone:
                self.waterfallGreen.interactFunc(self.waterfallGreenSound)
            if events.inDummyZone:
                self.dummy.interactFunc(self.dummySound)

            if events.inStatueZone:
                print("Player X =", self.playerActor.getX())
                if self.playerActor.getX() < 0:
                    if self.statue.interactFunc(self.statue, "forwards"):
                        messenger.send("solved")
                elif self.playerActor.getX() > 0:
                    if self.statue.interactFunc(self.statue, "backwards"):
                        messenger.send("solved")
            
            events.x = False

        if events.solved:
            self.waterfallGreen.object.model.setPos(6,-8,200)

        return Task.cont
    
    #Brought from Mario project. Uses trig funcs to calculate the coordinates the player should move to when WASD is pressed or jump (NYI) when space is pressed
    def __moveCalc__(self, WASD):
        jumping = False
        moves = []
        if (WASD == 'd'):
            tempRot = (self.playerActor.getH()) * (pi/180)
        elif (WASD == 's'):
            tempRot = (self.playerActor.getH() + 270) * (pi/180)
        elif (WASD == 'a'):
            tempRot = (self.playerActor.getH() + 180) * (pi/180)
        elif (WASD == 'w'):
            tempRot = (self.playerActor.getH() + 90) * (pi/180)
        elif (WASD == ' '):
            jumping = True

        if (jumping): #NYI
            self.gravity.addVelocity(15)
            moves.append(0) #very hacky, I know. This was brought from the Mario project and implemtation here was very much a 'shotgun' approach to get working
            moves.append(0)
            moves.append(0)
            print("Grounded", self.gravity.velocity)
            #println("jumping")
        else:
            moves.append(round(-20*cos(tempRot))/300) # Y
            moves.append(round(20*sin(tempRot))/300) # X
            moves.append(0) # Z
            #print("Moving by", moves[0], moves[1])
        
        return moves

    # ##"Event" Funcs

    #prints the player's x,y,z
    def debug(self):
        print("player is at",self.playerActor.getX(), self.playerActor.getY(), self.playerActor.getZ())
    
    #updates the camera's position and rotation
    def updateCamera(self):
        self.camera.setPos(-5, 0, self.cameraHeight)
        self.camera.setHpr(270, self.cameraPitch, 0 )

    #starts looping an animation
    def startAnim(self, animName):
        if self.playerActor.getCurrentAnim() != animName:
            self.playerActor.loop(animName)
            #self.playerActor.setPlayRate(2.0, animName)

    #moves the player with WASD. Movement when rotated is calculated with moveCalc
    def move(self, key):
        moves = self.__moveCalc__(key)
        if moves[0]+moves[1]+moves[2] != 0:
            self.playerActor.setPos(self.playerActor.getX()+moves[1], self.playerActor.getY()+moves[0], self.playerActor.getZ()+moves[2])

    #rotates the player when the 'q' or 'e' key is pressed
    def rotate(self, key):
        if (key == 'q'):
            self.playerActor.setH(self.playerActor.getH()+1)
        elif (key == 'e'):
            self.playerActor.setH(self.playerActor.getH()-1)




app = MyApp()



# ##RUN###
#Must remain last
app.run()