from aerforge import *

class Gravity:
    def __init__(self, object, gravity = 0.7, air_friction = 1, ground_friction = 20):
        self.object = object

        self.objects = []

        self.state = False
        self.grounded = False
        self.velocity_x = 0
        self.velocity_y = 0

        self.friction = 0
        self.air_friction = air_friction
        self.ground_friction = ground_friction

        self.gravity = gravity

    def force(self, force_x, force_y):
        self.velocity_x = self.velocity_x + force_x
        self.velocity_y = self.velocity_y + force_y

    def add_object(self, object):
        self.objects.append(object)

    def remove_object(self, object):
        self.objects.pop(self.objects.index(object))

    def update(self):
        self.object.x = self.object.x + self.velocity_x
        self.object.y = self.object.y + self.velocity_y

        self.state = False

        for i in self.objects:
            if not i.destroyed:
                if self.object.hit(i):
                    self.object.y = i.y - self.object.height + 1
                    self.velocity_y = 0
                    self.grounded = True
                    self.state = True

        if not self.state:
            self.grounded = False

        self.state = False

        if self.grounded:
            self.friction = self.air_friction + self.ground_friction

        else:
            self.friction = self.air_friction

        if self.velocity_x != 0:
            self.velocity_x = self.velocity_x / self.friction

        if not self.grounded:
            self.velocity_y = self.velocity_y + self.gravity