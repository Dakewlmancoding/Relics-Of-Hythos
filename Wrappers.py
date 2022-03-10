
#handles static geometry
class Geom():
    #String Path: Path to model, Array scale: x,y,z amount to scale the model (if only one value, then scale each axis by it), Bool Collision, Int XPos, Int YPos, Int ZPos,
    def __init__(self, path, scale, loader, xPos=0, yPos=0, zPos=0):
        self.xPos = xPos
        self.yPos = yPos
        self.zPos = zPos

        self.model = loader.loadModel(path)

        if len(scale) == 1:
            self.model.setScale(scale[0],scale[0],scale[0])
        else:
            self.model.setScale(scale[0],scale[1],scale[2])
        self.model.setPos(xPos, yPos, zPos)

    #reparents the model to a renderer (i.e. puts the object in the scene)
    def render(self, renderer):
        self.model.reparentTo(renderer)