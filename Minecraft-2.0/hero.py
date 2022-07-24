from direct.showbase.ShowBase import ShowBase


button_changeView = 'c'
button_switchMode = 'z'

button_turn_left = 'arrow_left'
button_turn_right = 'arrow_right'

button_go_back = 's'
button_go_right = 'd'
button_go_forward = 'w'
button_go_left = 'a'
button_up = 'e'
button_down = 'q'

button_place_block = 'b'
button_remove_block = 'v'

button_save_map = 'k'
button_load_map = 'l'


class Hero:
    def __init__(self, pos, land):
        self.land = land
        self.cameraOn = False
        self.mode = True

        self.hero = loader.loadModel('smiley')
        self.hero.setColor(1, .5, 0)
        self.hero.setScale(.3)
        self.hero.setPos(pos)

        self.hero.reparentTo(render)
        self.cameraBind()
        self.accept_events()

    def cameraBind(self):
        base.disableMouse()
        base.camera.reparentTo(self.hero)
        base.camera.setPos(0, 0, 1.5)
        self.cameraOn = True

    def cameraUp(self):
        pos = self.hero.getPos()
        base.mouseInterfaceNode.setPos(-pos[0], -pos[1], -pos[2]-3)
        base.camera.reparentTo(render)
        base.enableMouse()
        self.cameraOn = False


    def changeView(self):
        if self.cameraOn:
            self.cameraUp()
        else:
            self.cameraBind()

    def turn_left(self):
        self.hero.setH((self.hero.getH() + 5) % 360) 

    def turn_right(self):
        self.hero.setH((self.hero.getH() - 5) % 360)

    def look_at(self, angle):
        x_from = round(self.hero.getX())
        y_from = round(self.hero.getY())
        z_from = round(self.hero.getZ())

        dx, dy = self.check_dir(angle)
        x_to = x_from + dx
        y_to = y_from + dy
        return x_to, y_to, z_from

    def just_move(self, angle):
        pos = self.look_at(angle)
        self.hero.setPos(pos)

    def move_to(self, angle):
        if self.mode:
            self.just_move(angle)
        else:
            self.try_move(angle)
    
    def check_dir(self,angle):
        if angle >= 0 and angle <= 20:
            return (0, -1)
        elif angle <= 65:
            return (1, -1)
        elif angle <= 110:
            return (1, 0)
        elif angle <= 155:
            return (1, 1)
        elif angle <= 200:
            return (0, 1)
        elif angle <= 245:
            return (-1, 1)
        elif angle <= 290:
            return (-1, 0)
        elif angle <= 335:
            return (-1, -1)
        else:
            return (0, -1)

    def back(self):
        angle =(self.hero.getH()) % 360
        self.move_to(angle)

    def forward(self):
        angle = (self.hero.getH()+180) % 360
        self.move_to(angle)
    
    def right(self):
        angle = (self.hero.getH() + 90) % 360
        self.move_to(angle)

    def left(self):
        angle = (self.hero.getH() + 270) % 360
        self.move_to(angle)

    def changeMode(self):
        if self.mode:
            self.mode = False
        else:
            self.mode = True

    
    def try_move(self, angle):
        pos = self.look_at(angle)
        if self.land.isEmpty(pos):
            pos = self.land.findHighestEmpty(pos)
            self.hero.setPos(pos)
        else:
            pos = pos[0], pos[1], pos[2] + 1
            if self.land.isEmpty(pos):
                self.hero.setPos(pos)
    def up(self):
        if self.mode:
            self.hero.setZ(self.hero.getZ() + 1)

    def down(self):
        if self.mode and self.hero.getZ() > 1:
            self.hero.setZ(self.hero.getZ() - 1)
    
    def build(self):
        angle = self.hero.getH() % 360
        pos = self.look_at(angle)
        if self.mode:
            self.land.addBlock(pos)
        else:
            self.land.buildBlock(pos)

    def destroy(self):
        angle = self.hero.getH() % 360
        pos = self.look_at(angle)
        if self.mode:
            self.land.delBlock(pos)
        else:
            self.land.delBlockFrom(pos)

    def accept_events(self):
        base.accept(button_changeView, self.changeView)
        base.accept(button_switchMode, self.changeMode)

        base.accept(button_turn_left, self.turn_left)
        base.accept(button_turn_left + '-repeat', self.turn_left)
        base.accept(button_turn_right, self.turn_right)
        base.accept(button_turn_right + '-repeat', self.turn_right)

        base.accept(button_go_back, self.back)
        base.accept(button_go_back + '-repeat', self.back)
        base.accept(button_go_right, self.right)
        base.accept(button_go_right + '-repeat', self.right)
        base.accept(button_go_forward, self.forward)
        base.accept(button_go_forward + '-repeat', self.forward)
        base.accept(button_go_left, self.left)
        base.accept(button_go_left + '-repeat', self.left)

        base.accept(button_up, self.up)
        base.accept(button_up + '-repeat', self.up)
        base.accept(button_down, self.down)
        base.accept(button_down + '-repeat', self.down)

        base.accept(button_remove_block, self.destroy)
        base.accept(button_place_block, self.build)

        base.accept(button_load_map, self.land.loadMap)
        base.accept(button_save_map, self.land.saveMap)
