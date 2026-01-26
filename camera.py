from pygame.rect import Rect

DIS_WIDTH = 800
DIS_HEIGHT = 600


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
        l, t = -l + DIS_WIDTH / 2, -t + DIS_HEIGHT / 2
        l = min(0, l)
        t = max(-(camera.width - DIS_WIDTH), l)
        t = min(0, t)
        t = max(-(camera.height - DIS_HEIGHT), t)

        return Rect(l, t, w, h)
