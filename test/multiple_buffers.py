import sys
from pathlib import Path

sys.path.append(str(Path(__file__).absolute().parent.parent))

from spt_gfx import Screen, Buffer, KeyEvent, color, Key


def main():

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
        nonlocal currentStyleIndex, styles, currentStyle
        currentStyleIndex += 1
        currentStyleIndex %= len(styles)
        currentStyle = styles[currentStyleIndex]

    lorem = ""
    with open(Path(__file__).joinpath("../linux.txt").resolve(), "r") as file:
        lorem = file.read()

    content = Buffer()

    contentX = 1
    contentY = 1

    def contentUpdate(this: Buffer):
        nonlocal currentStyle
        this.clear()
        this.setTextWrapWords(contentX, contentY, currentStyle(lorem))
    content.update = contentUpdate
    content.setZ(1)
    screen.addBuffer(content)

    ui = Buffer()

    def uiUpdate(this: Buffer):
        this.clear()
        this.setString(
            1, this.getHeight(), color.bgWhite.black(
                "  enter: cycle styles    scroll: ↑/↓    ctrl+c: quit"
                + (" " * this.getWidth())
            )
        )
    ui.update = uiUpdate
    ui.setZ(2)
    screen.addBuffer(ui)

    def onKeyPressed(keyEvent: KeyEvent):
        nonlocal contentX, contentY
        if Key.ENTER in keyEvent.keys:
            cycleStyles()
            screen.refresh()
        if Key.UP in keyEvent.keys:
            contentY += 1
            screen.refresh()
        if Key.DOWN in keyEvent.keys:
            contentY -= 1
            screen.refresh()
        if Key.LEFT in keyEvent.keys:
            contentX += 1
            screen.refresh()
        if Key.RIGHT in keyEvent.keys:
            contentX -= 1
            screen.refresh()

    screen.addKeyListener(onKeyPressed)

    screen.refresh()

    return


if __name__ == "__main__":
    main()
