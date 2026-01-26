from PIL.FontFile import WIDTH
import blocks
import pyganim
from pygame import *
import monsters

ANIMATION_DELAY = 1
ANIMATION_RIGHT = [("pig/pig_right_1.png"), ("pig/pig_right_2.png")]
ANIMATION_LEFT = [("pig/pig_left_1.png"), ("pig/pig_left_2.png")]
ANIMATION_JUMP_LEFT = [("pig/pig_jump_left.png", ANIMATION_DELAY)]
ANIMATION_JUMP_RIGHT = [("pig/pig_jump_right.png", ANIMATION_DELAY)]
ANIMATION_JUMP = [("pig/pig_jump_right.png", ANIMATION_DELAY)]
ANIMATION_STAY = [("pig/pig_stay.png", ANIMATION_DELAY)]


MOVE_SPEED = 7
WIDTH = 32
HEIGHT = 22
COLOR = "#888888"
JUMP_POWER = 10
GRAVITY = 0.35
MOVE_EXTRA_SPEED = 2.5
JUMP_EXTRA_POWER = 1
ANIMATION_SUPER_SPEED_DELAY = 1.5


class Player(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.xvel = 0
        self.startX = x
        self.startY = y
        self.image = Surface((WIDTH, HEIGHT))
        self.image.fill(color=COLOR)
        self.rect = Rect(x, y, WIDTH, HEIGHT)
        self.yvel = 0
        self.onGround = False
        boltAmim = []
        boltAmimSuperSpeed = []
        for anim in ANIMATION_RIGHT:
            boltAmim.append((anim, ANIMATION_DELAY))
            boltAmimSuperSpeed.append((anim, ANIMATION_SUPER_SPEED_DELAY))
        self.boltAnimRight = pyganim.PygAnimation(boltAmim)
        self.boltAnimRight.play()
        self.boltAnimRightSuperSpeed = pyganim.PygAnimation(boltAmimSuperSpeed)
        self.boltAnimRightSuperSpeed.play()
        boltAmim = []
        boltAmimSuperSpeed = []
        for anim in ANIMATION_LEFT:
            boltAmim.append((anim, ANIMATION_DELAY))
            boltAmimSuperSpeed.append((anim, ANIMATION_SUPER_SPEED_DELAY))
        self.boltAnimLeft = pyganim.PygAnimation(boltAmim)
        self.boltAnimLeft.play()
        self.boltAnimLeftSuperSpeed = pyganim.PygAnimation(boltAmimSuperSpeed)
        self.boltAnimLeftSuperSpeed.play()
        self.boltAnimStay = pyganim.PygAnimation(ANIMATION_STAY)
        self.boltAnimStay.play()
        self.boltAnimStay.blit(self.image, (0, 0))
        self.boltAnimJumpLeft = pyganim.PygAnimation(ANIMATION_JUMP_LEFT)
        self.boltAnimJumpLeft.play()
        self.boltAnimJumpRight = pyganim.PygAnimation(ANIMATION_JUMP_RIGHT)
        self.boltAnimJumpRight.play()
        self.winner = False

    def update(self, left, right, up, running, platform):
        if up:
            if self.onGround:
                self.yvel = -JUMP_POWER
                if running and (left or right):
                    self.yvel -= JUMP_EXTRA_POWER
        self.image.fill(color=COLOR)
        self.boltAnimJumpRight.blit(self.image, (0, 0))
        if left:
            self.xvel = -MOVE_SPEED
            self.image.fill(Color(COLOR))
            if running:
                self.xvel -= MOVE_EXTRA_SPEED
                if not up:
                    self.boltAnimLeftSuperSpeed.blit(self.image, (0, 0))
            else:
                if not up:
                    self.boltAnimLeft.blit(self.image, (0, 0))
            if up:
                self.boltAnimJumpLeft.blit(self.image, (0, 0))
            else:
                self.boltAnimLeft.blit(self.image, (0, 0))

        if right:
            self.xvel = MOVE_SPEED
            self.image.fill(color=COLOR)
            if running:
                self.xvel += MOVE_EXTRA_SPEED
                if not up:
                    self.boltAnimRightSuperSpeed.blit(self.image, (0, 0))
            else:
                if not up:
                    self.boltAnimRight.blit(self.image, (0, 0))
            if up:
                self.boltAnimJumpRight.blit(self.image, (0, 0))
            else:
                self.boltAnimRight.blit(self.image, (0, 0))

        if not (left or right):
            self.xvel = 0
            if not up:
                self.image.fill(color=COLOR)
                self.boltAnimStay.blit(self.image, (0, 0))

        if not self.onGround:
            self.yvel += GRAVITY
        self.onGround = False;
        self.rect.y += self.yvel
        self.collide(0, self.yvel, platform)
        self.rect.x += self.xvel
        self.collide(self.xvel, 0, platform)

    def collide(self, xvel, yvel, platform):
        for p in platform:
            if sprite.collide_rect(self, p):
                if xvel > 0:
                    self.rect.right = p.rect.left
                if xvel < 0:
                    self.rect.left = p.rect.right
                if yvel > 0:
                    self.rect.bottom = p.rect.top
                    self.onGround = True
                    self.yvel = 0
                if yvel < 0:
                    self.rect.top = p.rect.bottom
                    self.yvel = 0
                if isinstance(p, blocks.BlockDie) or isinstance(p, monsters.Monster):
                    self.die()
                elif isinstance(p, blocks.BlockTeleport):
                    self.teleporting(p.goX, p.goY)
                elif isinstance(p, blocks.FlagWin):
                    self.winner = True

    def die(self):
        time.wait(500)
        self.teleporting(self.startX, self.startY)

    def teleporting(self, goX, goY):
        self.rect.x = goX
        self.rect.y = goY