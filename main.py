import pygame
from blocks import Platform, BlockDie, FlagWin, BlockTeleport
from camera import Camera
from player import Player
from pygame import *
from monsters import Monster
import os

DIS_WIDTH = 1100
DIS_HEIGHT = 850
DISPLAY = (DIS_WIDTH, DIS_HEIGHT)
BACKGROUNT_COLOR = "#004400"

PLATFORM_WIDTH = 32
PLATFORM_HEIGHT = 32
PLATFORM_COLOR = "#FF6262"
playerX = 55
playerY = 44


def loadLevel():
    global playerX, playerY

    level.clear()
    commands = []

    path = os.path.join('pig', 'levels.txt')
    with open(path, "r") as levelFile:
        reading_map = False

        for raw in levelFile:
            line = raw.strip()

            if not line or line.startswith("/"):
                continue
            if line.startswith("["):
                reading_map = True
                continue
            if line.startswith("]"):
                reading_map = False
                continue
            if reading_map:
                endLine = line.find("|")
                if endLine != -1:
                    level.append(line[:endLine])
                else:
                    level.append(line)
                continue
            parts = line.split()
            if not parts:
                continue

            cmd = parts[0]

            if cmd == "player":
                playerX = int(parts[1])
                playerY = int(parts[2])

            elif cmd == "portal":
                tp = BlockTeleport(int(parts[1]), int(parts[2]),
                                   int(parts[3]), int(parts[4]))
                entities.add(tp)
                platform.append(tp)
                animatedEntities.add(tp)

            elif cmd == "monster":
                mn = Monster(int(parts[1]), int(parts[2]),
                             int(parts[3]), int(parts[4]),
                             int(parts[5]), int(parts[6]))
                entities.add(mn)
                platform.append(mn)
                monsters.add(mn)


def main():
    loadLevel()
    pygame.init()
    screen = pygame.display.set_mode(DISPLAY)
    pygame.display.set_caption("SuperPig")
    bg = Surface((DIS_WIDTH, DIS_HEIGHT))

    bg.fill(color=BACKGROUNT_COLOR)

    left = right = False
    up = False
    running = False

    hero = Player(playerX, playerY)
    entities.add(hero)

    timer = pygame.time.Clock()

    total_level_widht = len(level[0]) * PLATFORM_WIDTH

    total_level_height = len(level) * PLATFORM_HEIGHT

    camera = Camera(Camera.camera_configure, total_level_widht, total_level_height)
    camera.update(hero)

    x = y = 0
    for row in level:
        for col in row:
            if col == '-':
                pf = Platform(x, y)
                entities.add(pf)
                platform.append(pf)

            if col == '*':
                bd = BlockDie(x, y)
                entities.add(bd)
                platform.append(bd)

            if col == 'F':
                fl = FlagWin(x, y)
                entities.add(fl)
                platform.append(fl)
                animatedEntities.add(fl)

            x += PLATFORM_WIDTH
        y += PLATFORM_HEIGHT
        x = 0

    while 1:
        timer.tick(60)
        camera.update(hero)
        for e in pygame.event.get():
            if e.type == KEYDOWN and e.key == K_LEFT:
                left = True
            if e.type == KEYDOWN and e.key == K_RIGHT:
                right = True
            if e.type == KEYDOWN and e.key == K_SPACE:
                up = True
            if e.type == KEYDOWN and e.key == K_LSHIFT:
                running = True
            if e.type == KEYUP and e.key == K_RIGHT:
                right = False
            if e.type == KEYUP and e.key == K_LEFT:
                left = False
            if e.type == KEYUP and e.key == K_SPACE:
                up = False
            if e.type == KEYUP and e.key == K_LSHIFT:
                running = False
            if e.type == QUIT:
                raise SystemExit("QUIT")

        screen.blit(bg, (0, 0))
        hero.update(left, right, up, running, platform)
        if hero.winner:
            font = pygame.font.Font(None, 100)
            text = font.render("ТЫ ПОБЕДИЛ!", True, (255, 215, 0))
            rect = text.get_rect(center=(DIS_WIDTH // 2, DIS_HEIGHT // 2))
            screen.blit(text, rect)
        for e in entities:
            screen.blit(e.image, camera.apply(e))
        if not hero.winner:
            camera.update(hero)
            animatedEntities.update()
            monsters.update(platform)
        pygame.display.update()


level = []
entities = pygame.sprite.Group()
animatedEntities = pygame.sprite.Group()
monsters = pygame.sprite.Group()
platform = []

if __name__ == "__main__":
    main()
