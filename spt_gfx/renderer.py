from signal import signal, SIGWINCH
from typing import List

from .buffer import Buffer
from .output import Output


class Renderer:

    _out: Output
    _buffers: List[Buffer]

    def __init__(self, output: Output):
        self._out = output
        self._buffers = []
        signal(SIGWINCH, self._onResize)

    def _sortBuffers(self):
        self._buffers = sorted(self._buffers, key=lambda buffer: buffer.getZ())
        return

    def _onResize(self, *args):
        for buffer in self._buffers:
            buffer.resize()
        self.render()
        return

    def render(self):
        self._sortBuffers()
        self._out.clearScreen()
        for buffer in self._buffers:
            buffer.update(buffer)
            self._out.write("".join(buffer.getData()))
        self._out.setCurPos(1, 1)
        self._out.flush()
        return

    def addBuffer(self, buffer: Buffer):
        self._buffers.append(buffer)
        return

    def removeBuffer(self, buffer: Buffer):
        self._buffers.remove(buffer)
        return
