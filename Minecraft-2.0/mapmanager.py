from direct.showbase.ShowBase import ShowBase
import pickle


class Mapmanager():
    def __init__(self):
        self.model = 'block.egg'
        self.texture = 'block.png'
        self.colors =[(0.5, 0.3, 0.0, 1),
                      (0.2, 0.2, 0.3, 1),
                      (0.5, 0.5, 0.2, 1),
                      (0.0, 0.6, 0.0, 1)]


        self.block = loader.loadModel(self.model)
        self.block.setTexture(loader.loadTexture(self.texture))

        self.startNew()

    def startNew(self):
        self.land = render.attachNewNode('Land')

    def loadLand(self, filename):
        with open(filename) as file:
            y = 0
            for line in file:
                x = 0
                for z in line.split():
                    for z0 in range(int(z) + 1):
                        self.addBlock((x, y, z0))
                    x += 1
                y += 1
        return x, y

    def clear(self):
        self.land.removeNode()
        self.startNew()

    def addBlock(self, position):
        self.block = loader.loadModel(self.model)
        self.block.setTexture(loader.loadTexture(self.texture))
        self.block.setPos(position)
        self.block.setColor(self.getColor(position[2]))
        self.block.reparentTo(self.land)

    def getColor(self, z):
        if z < len(self.colors):
            return self.colors[z]
        return self.colors[-1]

    def findHighestEmpty(self, pos):
        x, y, z = pos
        z = 1
        while not self.isEmpty((x, y, z)):
            z += 1
        return x, y, z

    def isEmpty(self, pos):
        blocks = self.findBlocks(pos)
        if blocks:
            return False
        return True

    def findBlocks(self, pos):
        return self.land.findAllMatches("=at=" + str(pos))

    def loadMap(self):
        self.clear()
        with open('my_map.dat', 'rb') as fin:
            for i in range(pickle.load(fin)):
                self.addBlock(pickle.load(fin))

    def saveMap(self):
        blocks = self.land.getChildren()
        with open('my_map.dat', 'wb') as fout:
            pickle.dump(len(blocks), fout)
            for block in blocks:
                x, y, z = block.getPos()
                pos = (int(x), int(y), int(z))
                pickle.dump(pos, fout)

    def buildBlock(self, pos):
        x, y, z = pos
        new = self.findHighestEmpty(pos)
        if new[2] <= z + 1:
            self.addBlock(new)

    def delBlock(self, pos):
        for b in self.findBlocks(pos):
            b.removeNode()

    def delBlockFrom(self, pos):
        x, y, z = self.findHighestEmpty(pos)
        pos = x, y, z - 1
        for b in self.findBlocks(pos):
            b.removeNode()
