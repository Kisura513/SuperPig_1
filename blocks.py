import pyganim
from pygame import *
import os

PLATFORM_WIDTH = 30
PLATFORM_HEIGHT = 30
PLATFORM_COLOR = "#FF6262"
ICON_DIR = os.path.dirname(__file__)
ANIMATION_BLOCKTLEPORT = [('pig/portal1.png'), ('pig/portal2.png')]
ANIMATION_FLAG = [('pig/flag1.png'), ('pig/flag2.png')]


class Platform(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
        self.image.fill(color=PLATFORM_COLOR)
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)


class BlockDie(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        self.image = image.load(os.path.join(ICON_DIR, 'pig/block_die.png'))


class BlockTeleport(Platform):
    def __init__(self, x, y, goX, goY):
        Platform.__init__(self, x, y)
        self.goX = goX
        self.goY = goY
        boltAnim = []
        for anim in ANIMATION_BLOCKTLEPORT:
            boltAnim.append((anim, 1))
        self.boltAnim = pyganim.PygAnimation(boltAnim)
        self.boltAnim.play()

    def update(self):
        self.image.fill(Color(PLATFORM_COLOR))
        self.boltAnim.blit(self.image, (0, 0))


class FlagWin(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        boltAmin = []
        for anim in ANIMATION_FLAG:
            boltAmin.append((anim, 1))
        self.boltAnim = pyganim.PygAnimation(boltAmin)
        self.boltAnim.play()

    def update(self):
        self.image.fill(Color(PLATFORM_COLOR))
        self.boltAnim.blit(self.image, (0, 0))
