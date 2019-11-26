import sys
from pathlib import Path

sys.path.append(str(Path(__file__).absolute().parent.parent))

from spt_gfx import Screen, Window, KeyEvent, color, Key


def main():

    screen = Screen()
    screen.open()

    lorem = ""
    with open(Path(__file__).joinpath("../lorem_ipsum.txt").resolve(), "r") as file:
        lorem = file.read()

    win1 = Window(5, 5, 50, 6)

    def win1Update(this: Window):
        this.clear()
        this.setTextWrapWords(1, 1, color.yellow.bold(lorem))

    win1.update = win1Update
    win1.setZ(5)
    screen.addBuffer(win1)

    win2 = Window(20, 9, 50, 6)

    def win2Update(this: Window):
        this.clear()
        this.setTextWrapWords(1, 1, color.red.italic(lorem))

    win2.update = win2Update
    win2.setBg(color.bgWhite)
    win2.setZ(4)
    screen.addBuffer(win2)

    def onKeyPressed(e: KeyEvent):
        # space: Toggle z-values
        if e.value == " ":
            z1 = win1.getZ()
            win1.setZ(win2.getZ())
            win2.setZ(z1)
            screen.refresh()

        # arrows: move win2
        if Key.UP in e.keys:
            win2.modY(-1)
            screen.refresh()
        if Key.RIGHT in e.keys:
            win2.modX(1)
            screen.refresh()
        if Key.DOWN in e.keys:
            win2.modY(1)
            screen.refresh()
        if Key.LEFT in e.keys:
            win2.modX(-1)
            screen.refresh()

        # shift_arrows: resize win2
        if Key.SHIFT_UP in e.keys:
            win2.modHeight(-1)
            screen.refresh()
        if Key.SHIFT_RIGHT in e.keys:
            win2.modWidth(1)
            screen.refresh()
        if Key.SHIFT_DOWN in e.keys:
            win2.modHeight(1)
            screen.refresh()
        if Key.SHIFT_LEFT in e.keys:
            win2.modWidth(-1)
            screen.refresh()
        pass

    screen.addKeyListener(onKeyPressed)

    screen.refresh()

    return


if __name__ == "__main__":
    main()
