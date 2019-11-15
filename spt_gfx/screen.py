import asyncio
from typing import Callable

from .buffer import Buffer
from .event import Event
from .input import Input, Key, KeyPress
from .output import Output
from .renderer import Renderer


class Screen(Buffer):

    _out: Output
    _renderer: Renderer
    _closeRequested: bool = False

    def __init__(self):
        super().__init__()
        self._out = Output()
        self._renderer = Renderer(self._out)
        self._renderer.addBuffer(self)
        return

    def open(self):

        async def run():
            await self._listen()

        self._out.enterAltBuffer()
        self._out.enableAutoWrap(False)
        self._out.hideCursor()
        self._out.flush()
        loop = asyncio.get_event_loop()
        if loop.is_running():
            loop.create_task(run())
        else:
            loop.run_until_complete(run())

    def close(self):
        self._out.exitAltBuffer()
        self._out.enableAutoWrap(True)
        self._out.showCursor()
        self._out.flush()
        self._closeRequested = True
        return

    def refresh(self):
        self._renderer.render()
        return

    async def _listen(self):
        while not self._closeRequested:
            keyPress = Input.getKey()
            if keyPress.key in (Key.CTRL_C, Key.CTRL_D):
                self.close()
                break
            self._eventHandler.trigger(Event.KEY_PRESSED, keyPress)

    def addBuffer(self, buffer: Buffer):
        self._renderer.addBuffer(buffer)
        return

    def removeBuffer(self, buffer: Buffer):
        self._renderer.removeBuffer(buffer)
        return

    def addKeyListener(self, callback: Callable[[KeyPress], None]):
        self._eventHandler.on(Event.KEY_PRESSED, callback)
        return

