from pygame.rect import Rect

SCREEN_WIDTH = 1100
SCREEN_HEIGHT = 850


class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)

    def camera_configure(camera, target_rect):
        l, t, _, _ = target_rect
        _, _, w, h = camera

        l = -l + SCREEN_WIDTH // 2
        t = -t + SCREEN_HEIGHT // 2

        l = min(0, l)
        t = min(0, t)

        l = max(-(camera.width - SCREEN_WIDTH), l)
        t = max(-(camera.height - SCREEN_HEIGHT), t)

        return Rect(l, t, w, h)