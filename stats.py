

class Stat:
    def __init__(self):
        self.x = 3.0
        self.reason = None

    def dec(self, dx, reason=None, sound=None):
        if reason and self.x > -3.0:
            self.reason = reason
        self.x -= dx
        if self.x <= -3.0: self.x = -3.0

        if sound:
            sound.play("windnoise", dur=max(dx, 0.1))

    def inc(self, dx):
        self.x += dx
        if self.x > 3.0: self.x = 3.0

class Stats:
    def __init__(self):
        self.health = Stat()
        self.sleep = Stat()
        self.tired = Stat()
        self.hunger = Stat()
        self.thirst = Stat()
        self.warmth = Stat()


