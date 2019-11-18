import re
from os import get_terminal_size
from typing import List, Callable

from .event import Event
from .event_handler import EventHandler


def _filter(string: str) -> str:
    return re.sub(r"[\n\r]", "", str(string))


class Buffer:

    _eventHandler: EventHandler
    _data: List[str]
    _width: int
    _height: int
    _z: int
    update: Callable = lambda *args: args

    def __init__(self):
        self._eventHandler = EventHandler()
        self._data = []
        size = get_terminal_size()
        self._width = size.columns
        self._height = size.lines
        self._z = 0

    def resize(self):
        size = get_terminal_size()
        self._width = size.columns
        self._height = size.lines
        return

    def clear(self):
        self._data = []
        return

    def _setCurPos(self, x: int, y: int):
        self._data.append(f"\x1b[{y};{x}H")
        return

    def setString(self, x: int, y: int, data: str):
        if x <= self._width and 1 <= y <= self._height:
            self._setCurPos(x, y)
            self._data.append(_filter(data))
        return

    def setText(self, x: int, y: int, data: str):
        if x < self._width and 1 <= y < self._height:
            lines: List[str] = data.split("\n")
            for i in range(len(lines)):
                if len(lines[i]) > 0:
                    self.setString(x, y + i, lines[i])
        return

    def setTextWrap(self, x: int, y: int, data: str):
        if len(data) == 0:
            return
        limit: int = self.getWidth() - x + 1
        ci = 0
        xOffset = 0
        lineOffset = 0
        line = ""
        while ci < len(data):
            char: str = data[ci]
            xOffset += 1
            if xOffset == limit or char == "\n":
                self.setString(x, y + lineOffset, line)
                lineOffset += 1
                xOffset = 0
                line = ""
                if char == "\n":
                    ci += 1
                continue
            ci += 1
            line += char
        if len(line) > 0:
            self.setString(x, y + lineOffset, line)
        return

    def getData(self) -> List[str]:
        return self._data

    def getWidth(self) -> int:
        return self._width

    def getHeight(self) -> int:
        return self._height

    def getZ(self) -> int:
        return self._z

    def setZ(self, value: int):
        self._z = value
        return
