import pyglet
from pyglet import clock

display = pyglet.window.get_platform().get_default_display()
screens = display.get_screens()
window = pyglet.window.Window(fullscreen=True, screen=screens[1])

label = pyglet.text.Label('Hello, world',
                  font_name='Times New Roman',
                  font_size=36,
                  x=window.width//2, y=window.height//2,
                  anchor_x='center', anchor_y='center')


@window.event
def on_draw():
    window.clear()
    label.draw()


@window.event
def on_key_press(symbol, modifiers):
    if symbol == pyglet.window.key.ESCAPE:
        pyglet.app.exit()
    if symbol == pyglet.window.key.ENTER:
        hide_text(label, 2)

def hide_text(label, time):
    clock.schedule_interval(set_label_opacity, 1/10.0)

def set_label_opacity(label, opacity):
    label.color(label.color[0], label.color[1], label.color[2], opacity)

pyglet.app.run()
