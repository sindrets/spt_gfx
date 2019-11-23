
# Simple Python Terminal Graphics

`spt_gfx` is a small, lightweight framework that is designed to give you a simple, yet fast and powerful way to access the alternate buffer and create graphics in the terminal.

> Note: Only works with ANSI terminals. This framework heavily relies on ANSI control sequences, and I'm not really interested in supporting Windows.

### Installation
```sh
sudo python3 setup.py install
```

### Usage

Following is a simple example of how to draw some text to the screen and attach a key listener.

```python
from spt_gfx import Screen, KeyEvent

screen = Screen()
screen.open()

screen.setTextWrap(
    10, 5,
    "This text is written directly to the screen, and will disappear on"
    + "the next screen clear."
)

def screenUpdate(this: Screen):
    this.setTextWrap(
        10, 9,
        "This text is written from the screen's update method, and will "
        + "persist over screen refreshes."
    )

screen.update = screenUpdate

def onKeyPressed(keyEvent: KeyEvent):
    screen.clear()
    screen.setString(1, 1, str(keyEvent))
    screen.refresh()

screen.addKeyListener(onKeyPressed)

screen.refresh()
```

The `screen.open()` method initializes the screen and opens the alternate buffer. You leave the alternate buffer and dispose of the screen by calling the `screen.close()` method. By default this method is called when pressing ctrl+c or ctrl+d, but this can be intercepted in a key  listener by calling `keyEvent.invalidate()`.

The `screen.update` property is a callable that is a called on each screen refresh. This property exists on all `Buffer` objects.

The `screen.refresh()` method will first call every buffer's update method before rendering all pending draw events to the screen.

There are four methods for drawing text to the screen:

```python
buffer.setString(x: int, y: int, data: str)
```

This method is used for modifying a single line in the buffer, and does not support newline characters. When reaching the end of the screen it will simply stop.

```python
buffer.setText(x: int, y: int, data: str)
```

This method supports newline characters and new lines will start from the same x-value as the initial line.

```python
buffer.setTextWrap(x: int, y: int, data: str)
```

This method supports newline characters and will also automatically hard-wrap text that reaches the end of the screen.

```python
buffer.setTextWrapWords(x: int, y: int, data: str)
```

This is similar to the `setTextWrap` method, but this will sensibly wrap words.

### Using multiple Buffer objects

The following is an example of how to use multiple buffer objects. This example, along with the `lorem_ipsum.txt` file can be located in `./test`.

```python
from spt_gfx import Screen, Buffer, KeyEvent, color, Key
from pathlib import Path

screen = Screen()
screen.open()

styles = [
    color.yellow.bold,
    color.red.italic,
    color.green.underline
]
currentStyleIndex = 0
currentStyle = styles[currentStyleIndex]

def cycleStyles():
    global currentStyleIndex, styles, currentStyle
    currentStyleIndex += 1
    currentStyleIndex %= len(styles)
    currentStyle = styles[currentStyleIndex]

lorem = ""
with open(Path(__file__).joinpath("../lorem_ipsum.txt").resolve(), "r") as file:
    lorem = file.read()

content = Buffer()

def contentUpdate(this: Buffer):
    this.clear()
    this.setTextWrap(1, 1, currentStyle(lorem))
content.update = contentUpdate
content.setZ(1)
screen.addBuffer(content)

ui = Buffer()

def uiUpdate(this: Buffer):
    this.clear()
    this.setString(
        1, this.getHeight(), color.bgWhite.black(
            "  enter: cycle styles  ctrl+c: quit"
            + (" " * this.getWidth())
        )
    )
ui.update = uiUpdate
ui.setZ(2)
screen.addBuffer(ui)

def onKeyPressed(keyEvent: KeyEvent):
    if Key.ENTER in keyEvent.keys:
        cycleStyles()
        screen.refresh()

screen.addKeyListener(onKeyPressed)

screen.refresh()
```

The `buffer.setZ()` method adjusts the buffer's z-index. The z-index determines the order in which the buffers are drawn to the screen. Buffers with higher z values are drawn over buffers with lower z values.

On screen refresh, the renderer merges the data from all buffers into a temporary buffer before all data is drawn to the screen in a single print call. This helps minimize any flashing that might occur if the buffers are drawn to the screen in sequence. 

### Text styling

Included in the framework is a text styling utility that is heavily inspired by [chalk](https://github.com/chalk/chalk). The usage is simple:

```python
from spt_gfx import color
print(color.yellow("Foo bar."))
```

And just like chalk, the API calls are chainable:

```python
print(color.yellow.bgCyan.italic.underline("Foo bar."))
```

For terminals that support truecolor you can also use RGB:

```python
print(color.bgRgb(233, 30, 99)("Foo bar."))
```
