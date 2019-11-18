import sys
from pathlib import Path

sys.path.append(str(Path(__file__).absolute().parent.parent))

from time import time_ns
from threading import Thread

from spt_gfx import Screen, KeyEvent, Key
from spt_gfx import Buffer
from spt_gfx import color


def main():
    screen: Screen = None

    try:
        totalFrameCount: int = 0
        totalChars: int = 0
        frames: int = 0
        fps: int = 0
        last: int = 0
        running: bool = False

        screen = Screen()
        screen.open()

        content = ""
        for y in range(screen.getHeight()):
            content += ("@" * screen.getWidth())
            if y < screen.getHeight():
                content += "\n"
        totalChars += len(content)

        def screenUpdate(this: Screen):
            nonlocal totalFrameCount, frames, fps, last
            totalFrameCount += 1
            frames += 1
            this.clear()
            this.setText(1, 1, content)
            if (time_ns() / 1_000_000) - last >= 1000:
                fps = frames
                frames = 0
                last += 1000
            return
        screen.update = screenUpdate

        info = Buffer()

        def infoUpdate(this: Buffer):
            this.clear()
            this.setString(1, this.getHeight() - 1,
                           color.bgWhite.black(
                               f"  total frame count: {totalFrameCount}    "
                               f"fps: {fps}    chars drawn per frame: {totalChars}")
                           + color.bgWhite(" " * this.getWidth())
                           )
            this.setString(1, this.getHeight(),
                           color.bgWhite.black("  start/stop diagnostic: enter")
                           + color.bgWhite(" " * this.getWidth())
                           )
            return
        info.update = infoUpdate
        info.setZ(2)
        screen.addBuffer(info)

        def runDiagnostic():
            nonlocal running, last
            last = time_ns() / 1_000_000
            while running:
                screen.refresh()
            return

        def onKeyPressed(keyEvent: KeyEvent):
            nonlocal running
            if Key.ENTER in keyEvent.keys:
                running = not running
                if running:
                    Thread(target=runDiagnostic).start()

        screen.addKeyListener(onKeyPressed)

        screen.refresh()

    except:
        if screen is not None:
            screen.close()
    return


if __name__ == "__main__":
    main()
