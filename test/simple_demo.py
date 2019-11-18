import sys
from pathlib import Path

sys.path.append(str(Path(__file__).absolute().parent.parent))

from spt_gfx import Screen, KeyEvent
from spt_gfx import color
import logging
import traceback

if __name__ == "__main__":
    screen: Screen = None

    try:
        screen = Screen()
        screen.open()

        screen.setTextWrap(10, 5, color.yellow.bgCyan.italic.underline(
            "This text is written directly to the screen, and will disappear on the next screen refresh."
        ))


        def screenUpdate(this: Screen):
            this.setTextWrap(
                10, 9,
                "This text is set in the screen's update method, and will persist over screen refreshes."
            )

        screen.update = screenUpdate

        def onKeyPressed(keyEvent: KeyEvent):
            screen.clear()
            screen.setString(1, 1, str(keyEvent))
            screen.refresh()

        screen.addKeyListener(onKeyPressed)

        screen.refresh()
    except:
        if screen is not None:
            screen.close()
        logging.error(traceback.format_exc())
