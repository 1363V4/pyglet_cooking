from optparse import NO_DEFAULT
import pyglet

# SETTINGS

pyglet.resource.path = ['resources']
pyglet.resource.reindex()

# UTILS

def center_image(image):
    """Sets an image's anchor point to its center"""
    image.anchor_x = image.width // 2
    image.anchor_y = image.height // 2

# GAME

# attention faut définir la window avant les sprites
window = pyglet.window.Window(960, 540)

sun = pyglet.resource.image("sun.png")
sun_seq = pyglet.image.ImageGrid(sun, 3, 5)
print(type(sun))
sun_sprite = pyglet.sprite.Sprite(sun, x=50, y=50)
print(type(sun_sprite))


sun_seq_index = 0

def update(dt):
    global sun_seq_index
    sun_seq_index += 1
    sun_seq_index %= 3
    sun_seq_index = int(sun_seq_index)

pyglet.clock.schedule_interval(update, 1/10.0)

@window.event
def on_draw():
    window.clear()
    sun_seq[sun_seq_index].blit(window.width // 2, window.height // 2)
    sun_sprite.draw()

if __name__ == '__main__':
    pyglet.app.run()


# from array import array

# # Approach 1
# # Using a magic number
# NO_ENTITIES = 128
# x = array('B', [101] * NO_ENTITIES)
# y = array('B', [101] * NO_ENTITIES)

# for i in range(NO_ENTITIES):
#     if x[i] == 101:
#         continue
#     process() 

# # Approach 2
# # Using a boolean array
# NO_ENTITIES = 128
# b = array('B', [0] * NO_ENTITIES)
# x = array('B', [0] * NO_ENTITIES)
# y = array('B', [0] * NO_ENTITIES)

# for i in range(NO_ENTITIES):
#     if not b[i]:
#         continue
#     process() 

# # Approach 3
# # Dynamic arrays
# NO_ENTITIES = 128
# x = array('B')
# y = array('B')

# for i in range(len(x)):
#     process() 