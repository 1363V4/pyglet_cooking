---
title: i love pyglet
layout: post
---

## introduction

so here i was with a problem.

i wanted to make an animated sun bounce around my screen.

(by the end of the article you will know how to make yours too!)

something like this:

video

with some added constraints:
- i wanted to spawn/despawn suns
- i wanted the suns to be animated
- i could place some elements and suns would bounce off them

why?
well i do youtube videos,
twitch streaming,
and you know how the kids are,
easily distracted unless you have a 
steady supply of dopamine.

did it work? hell yeah, look at that!

video

now, to make this happen,
i would need a piece of software that could:
- handle input
- advance state
- draw stuff

we usually call these things
"game engines".
the name is fairly transparent.

i have some experience with pygame
(and watch da fluffy potato's videos),
but before diving in i made a qujick google search
and found **pyglet**.

it seemed less cumbersome than pygame,
and after dev'ing with it i can say it is.
mostly because:
- no external dependencies
- nice writing style, doesn't feel "bloated"
- lot of simple optimizations out-of-the-box (batching, animations)
- the event system is versatile (simple defaults for controls or window, but can be easily extended)
- ...

i could go on, but code is worth a thousand word.

let's go!

## how to make funny suns

so the trick here
is to use a blue screen
(just like in marvel movies).

you draw your stuff on a blue background,
capture the window with 
[obs](),
then use the "alpha key" feature of obs to remove the blue.

here is what you see:

video

(the red box will be masked by our big fat head, don't worry)

so, let's go and draw a background.
the way we *connoisseurs* of the video art do it
is we draw a big fat rectangle on the screen:

```python
import pyglet


WINDOW_W = 1920
WINDOW_H = 1080


window = pyglet.window.Window(WINDOW_W, WINDOW_H, fullscreen=True)

background = pyglet.shapes.Rectangle(0, 0, WINDOW_W, WINDOW_H, color=(0, 0, 255))

@window.event
def on_draw():
    window.clear()
    background.draw()

if __name__ == "__main__":
    pyglet.app.run()
```

i just love that i don't have to explain anything.
pyglet "hello world" is very self-explanatory,
especially if you're familiar with decorators and event systems
(for example if you did some webdev).

if it doesn't click, just stare at it a bit longer,
i promise it will.

"rectangle" is not the only cool helper you get,
you have all them shapes + text too:

```python

count_label = pyglet.text.Label(
    "louis sunshine",
    font_name="Arial",
    font_size=16,
    x=10,
    y=WINDOW_H - 34,
    anchor_x="left",
    anchor_y="top",
    color=(255, 255, 255, 255),
)

# later...

@window.event
def on_draw():
    window.clear()
    background.draw()
    count_label.draw()
```

notice how anchor
(the "reference" point of the element)
can be nicely set up with shorthands.

okay, that's nice and jazzy,
but what about the suns?

well, we're going to use this spritesheet:

![sun]()

like this:

```python
# this tells pyglet that folder "resources" is where we dump our assets
pyglet.resource.path = ["resources"]
pyglet.resource.reindex()

# we load the image and indicate the grid size
sun_image = pyglet.resource.image("sun2.png")
sun_grid  = pyglet.image.ImageGrid(sun_image, 1, 6)

# center the anchor
for frame in sun_grid:
    frame.anchor_x = frame.width  // 2
    frame.anchor_y = frame.height // 2

# turn the frames into a looping animation (0.1 s per frame)
sun_animation = pyglet.image.animation.Animation.from_image_sequence(
    sun_grid, duration=0.1, loop=True
)

# there you have it
# and you'll use the animation like this:
sprite = pyglet.sprite.Sprite(sun_animation, batch=batch)
```

hold on, what is that "batch" thing?

remember how we drew the background first,
**then** the text?
this was for the background not to be over the text.

batch mostly means 
"these things, i don't care if they overlap, draw them in one go"
and it speeds the rendering by quite a lot.

now let's make the suns move around!

```python
# let's pretend we have a function update_sun
# which takes dt (amount of time passed) as an argument
def update_sun(sun, dt):
    ...
    # here, we compute the new position of the sun
    # based on its initial position, velocity
    # and, importantly, dt!

# we then only have to attach this function to a clock
# so the function is called every dt
pyglet.clock.schedule_interval(update, 1 / 60.0)
```

the last thing we need to do is to handle inputs.

```python

@window.event
def on_key_press(symbol, modifiers):
    if symbol == pyglet.window.key.SPACE:
        spawn_sun()
    elif symbol == pyglet.window.key.BACKSPACE:
        remove_last_sun()
```

once again, very straightforward
with pyglet's good defaults.

---

okay, thanks for sticking with me for so long.

this was not exactly a tutorial,
what i wanted was to show you the small building blocks.

these small "lego" blocks are all you need.
now it's time to put them together,
i will show you the big structure.
don't be scared by the collision code
(it's bad anyway)

here is the full code:

```python
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
    
```

---

i'll write more pyglet stuff in the future.
stay tuned in!
