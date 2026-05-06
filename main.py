import math
import random
import time

import pyglet

# SETTINGS
pyglet.resource.path = ["resources"]
pyglet.resource.reindex()

WINDOW_W = 1920
WINDOW_H = 1080

BOX_W = 460
BOX_H = 340
BOX_X = WINDOW_W - BOX_W
BOX_Y = 0

SUN_SPEED = 150

FRAME_DURATION = 0.1  # seconds per animation frame


def center_image(image):
    image.anchor_x = image.width // 2
    image.anchor_y = image.height // 2


# window = pyglet.window.Window(WINDOW_W, WINDOW_H)
window = pyglet.window.Window(WINDOW_W, WINDOW_H, fullscreen=True)
pyglet.gl.glClearColor(0, 0, 0, 1)

# sun_image = pyglet.resource.image("sun.png")
# sun_grid = pyglet.image.ImageGrid(sun_image, 2, 3)
sun_image = pyglet.resource.image("sun2.png")
sun_grid = pyglet.image.ImageGrid(sun_image, 1, 6)

# Center each frame's anchor point
for frame in sun_grid:
    center_image(frame)

# Build a proper Animation from all 15 frames
sun_animation = pyglet.image.animation.Animation.from_image_sequence(
    sun_grid, duration=FRAME_DURATION, loop=True
)

count_label = pyglet.text.Label(
    "",
    font_name="Arial",
    font_size=16,
    x=10,
    y=WINDOW_H - 34,
    anchor_x="left",
    anchor_y="top",
    color=(255, 255, 255, 255),
)

fps_display = pyglet.window.FPSDisplay(window)
bg = pyglet.shapes.Rectangle(0, 0, window.width, window.height, color=(0, 0, 255))
red_box = pyglet.shapes.Rectangle(BOX_X, BOX_Y, BOX_W, BOX_H, color=(0, 0, 255))
batch = pyglet.graphics.Batch()


class Sun:
    def __init__(self):
        angle = random.uniform(0, 2 * math.pi)
        self.vx = math.cos(angle) * SUN_SPEED
        self.vy = math.sin(angle) * SUN_SPEED

        # Temporary sprite to get dimensions for spawn check
        self.sprite = pyglet.sprite.Sprite(sun_animation, x=0, y=0, batch=batch)

        while True:
            x = random.uniform(50, WINDOW_W - 50)
            y = random.uniform(50, WINDOW_H - 50)
            if not self._inside_box(x, y):
                break

        self.sprite.x = x
        self.sprite.y = y

    def _inside_box(self, x, y):
        hw = self.sprite.width // 2
        hh = self.sprite.height // 2
        return (
            x + hw > BOX_X
            and x - hw < BOX_X + BOX_W
            and y + hh > BOX_Y
            and y - hh < BOX_Y + BOX_H
        )

    def _half_w(self):
        return self.sprite.width // 2

    def _half_h(self):
        return self.sprite.height // 2

    def update(self, dt):
        nx = self.sprite.x + self.vx * dt
        ny = self.sprite.y + self.vy * dt

        hw = self._half_w()
        hh = self._half_h()

        if nx - hw < 0:
            nx = hw
            self.vx = abs(self.vx)
        elif nx + hw > WINDOW_W:
            nx = WINDOW_W - hw
            self.vx = -abs(self.vx)

        if ny - hh < 0:
            ny = hh
            self.vy = abs(self.vy)
        elif ny + hh > WINDOW_H:
            ny = WINDOW_H - hh
            self.vy = -abs(self.vy)

        sx, sy = nx, ny
        if (
            sx + hw > BOX_X
            and sx - hw < BOX_X + BOX_W
            and sy + hh > BOX_Y
            and sy - hh < BOX_Y + BOX_H
        ):
            px, py = self.sprite.x, self.sprite.y
            overlap_x = min(px + hw - BOX_X, BOX_X + BOX_W - (px - hw))
            overlap_y = min(py + hh - BOX_Y, BOX_Y + BOX_H - (py - hh))

            if overlap_x < overlap_y:
                self.vx = -self.vx
                nx = self.sprite.x
            else:
                self.vy = -self.vy
                ny = self.sprite.y

        self.sprite.x = nx
        self.sprite.y = ny
        self.sprite.scale = 1 + 0.2 * math.cos(time.time())


suns = []


def spawn_sun(dt):
    suns.append(Sun())


def update(dt):
    for s in suns:
        s.update(dt)
    count_label.text = f"Suns: {len(suns)}"


pyglet.clock.schedule_interval(update, 1 / 60.0)
pyglet.clock.schedule_interval(spawn_sun, 60 * 10)
spawn_sun(0)


@window.event
def on_key_press(symbol, modifiers):
    match symbol:
        case pyglet.window.key.BACKSPACE:
            suns[-1].sprite.delete()
            suns.pop()
        case pyglet.window.key.SPACE:
            spawn_sun(0)
        case _:
            pass


@window.event
def on_draw():
    window.clear()
    bg.draw()
    red_box.draw()
    batch.draw()
    fps_display.draw()
    count_label.draw()


if __name__ == "__main__":
    pyglet.app.run()
