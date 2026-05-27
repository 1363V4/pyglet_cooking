import math
import random
import time

import pyglet


# SETTINGS 

pyglet.resource.path = ["resources"]
pyglet.resource.reindex()

WINDOW_W = 1920
WINDOW_H = 1080

# in pixels per second
SUN_SPEED = 150          
# seconds between automatic spawns
AUTO_SPAWN_SUN = 0.01   

# streamer box
BOX_W = 460
BOX_H = 340
BOX_X = WINDOW_W - BOX_W
BOX_Y = 0


# WINDOW 

window = pyglet.window.Window(WINDOW_W, WINDOW_H, fullscreen=True)

# SHAPES

background = pyglet.shapes.Rectangle(0, 0, WINDOW_W, WINDOW_H, color=(0, 0, 255))
red_box = pyglet.shapes.Rectangle(BOX_X, BOX_Y, BOX_W, BOX_H, color=(0, 0, 255))

# TEXT 

fps_display = pyglet.window.FPSDisplay(window)
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


#  SUN

sun_image = pyglet.resource.image("sun2.png")
sun_grid  = pyglet.image.ImageGrid(sun_image, 1, 6)

for frame in sun_grid:
    frame.anchor_x = frame.width  // 2
    frame.anchor_y = frame.height // 2

sun_animation = pyglet.image.animation.Animation.from_image_sequence(
    sun_grid, duration=0.1, loop=True
)


#  SUNS 

suns = []  # list of sun dicts

batch = pyglet.graphics.Batch()

def make_sun():
    x = random.uniform(100, WINDOW_W - BOX_W - 100)
    y = random.uniform(100, WINDOW_H - BOX_H - 100)

    sprite = pyglet.sprite.Sprite(sun_animation, x=x, y=y, batch=batch)

    angle = random.uniform(0, 2 * math.pi)
    vx = math.cos(angle) * SUN_SPEED
    vy = math.sin(angle) * SUN_SPEED
    phase = random.randint(1,234) # wobble offset

    return {"sprite": sprite, "vx": vx, "vy": vy, "phase": phase}


# we'll call it on a clock so dt has to be provided
# we attribute it to none to please the linter
def spawn_sun(dt=None):
    suns.append(make_sun())


def remove_last_sun():
    if suns:
        suns[-1]["sprite"].delete()  # free the sprite from video memory
        suns.pop()


#  UPDATE 

def update_sun(sun, dt):
    sprite = sun["sprite"]

    nx = sprite.x + sun["vx"] * dt
    ny = sprite.y + sun["vy"] * dt

    # Start of terrible collision code
    if nx < 0:
        sun["vx"] = abs(sun["vx"])      # push right
    elif nx > WINDOW_W:
        sun["vx"] = -abs(sun["vx"])     # push left

    if ny < 0:
        sun["vy"] = abs(sun["vy"])      # push up
    elif ny > WINDOW_H:
        sun["vy"] = -abs(sun["vy"])     # push down

    hits_box = (
        nx > BOX_X           and
        nx < BOX_X + BOX_W   and
        ny > BOX_Y           and
        ny < BOX_Y + BOX_H
    )
    if hits_box:
        if BOX_Y < sun["sprite"].y < BOX_Y + BOX_H:
            sun["vx"] = -sun["vx"]
        else:
            sun["vy"] = -sun["vy"]
    # End of terrible collision code

    sprite.x = nx
    sprite.y = ny

    # wobble effect oscillates between 0.8 and 1.2
    # with added random phase offset
    sprite.scale = 1 + 0.2 * math.cos(time.time() + sun["phase"])


def update(dt):
    for sun in suns:
        update_sun(sun, dt)
    count_label.text = f"Suns: {len(suns)}"


#  CLOCKS 

pyglet.clock.schedule_interval(update, 1 / 60.0)

# auto-spawn a sun every now and then
pyglet.clock.schedule_interval(spawn_sun, AUTO_SPAWN_SUN)

#  INPUT

@window.event
def on_key_press(symbol, modifiers):
    if symbol == pyglet.window.key.SPACE:
        spawn_sun()
    elif symbol == pyglet.window.key.BACKSPACE:
        remove_last_sun()

#  DRAW 

@window.event
def on_draw():
    window.clear()
    background.draw()
    red_box.draw()
    batch.draw()       # draws all sun sprites at once
    fps_display.draw()
    count_label.draw()


#  RUN

if __name__ == "__main__":
    pyglet.app.run()
