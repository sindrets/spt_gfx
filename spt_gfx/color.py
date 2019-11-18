from enum import Enum
from typing import List, Union


class AnsiStyle(Enum):
    RESET = u"\x1b[0m"
    BOLD = u"\x1b[1m"
    DIM = u"\x1b[2m"  # not widely supported
    ITALIC = u"\x1b[3m"  # not widely supported, sometimes treated as reverse
    UNDERLINE = u"\x1b[4m"
    REVERSED = u"\x1b[7m"  # swap foreground and background colors
    BLACK = u"\x1b[30m"
    RED = u"\x1b[31m"
    GREEN = u"\x1b[32m"
    YELLOW = u"\x1b[33m"
    BLUE = u"\x1b[34m"
    MAGENTA = u"\x1b[35m"
    CYAN = u"\x1b[36m"
    WHITE = u"\x1b[37m"
    BLACK_BRIGHT = u"\x1b[30;1m"
    RED_BRIGHT = u"\x1b[31;1m"
    GREEN_BRIGHT = u"\x1b[32;1m"
    YELLOW_BRIGHT = u"\x1b[33;1m"
    BLUE_BRIGHT = u"\x1b[34;1m"
    MAGENTA_BRIGHT = u"\x1b[35;1m"
    CYAN_BRIGHT = u"\x1b[36;1m"
    WHITE_BRIGHT = u"\x1b[37;1m"
    BG_BLACK = u"\x1b[40m"
    BG_RED = u"\x1b[41m"
    BG_GREEN = u"\x1b[42m"
    BG_YELLOW = u"\x1b[43m"
    BG_BLUE = u"\x1b[44m"
    BG_MAGENTA = u"\x1b[45m"
    BG_CYAN = u"\x1b[46m"
    BG_WHITE = u"\x1b[47m"
    BG_BLACK_BRIGHT = u"\x1b[40;1m"
    BG_RED_BRIGHT = u"\x1b[41;1m"
    BG_GREEN_BRIGHT = u"\x1b[42;1m"
    BG_YELLOW_BRIGHT = u"\x1b[43;1m"
    BG_BLUE_BRIGHT = u"\x1b[44;1m"
    BG_MAGENTA_BRIGHT = u"\x1b[45;1m"
    BG_CYAN_BRIGHT = u"\x1b[46;1m"
    BG_WHITE_BRIGHT = u"\x1b[47;1m"


class Style:

    ansiCode: str

    def __init__(self, ansiCode: Union[str, AnsiStyle]):
        code = ansiCode
        if isinstance(ansiCode, AnsiStyle):
            code = ansiCode.value
        self.ansiCode = code

    def __call__(self, text: str):
        return AnsiStyle.RESET.value + self.ansiCode + text + AnsiStyle.RESET.value


class Color:

    _styles: List[Style]

    def __init__(self):
        self._styles = []

    def __call__(self, text) -> str:
        result: str = ""
        for style in self._styles:
            result += style.ansiCode
        return AnsiStyle.RESET.value + result + text + AnsiStyle.RESET.value

    def _clone(self, newStyle: Style):
        clone = Color()
        clone._styles = self._styles.copy()
        if newStyle is not None:
            clone._styles.append(newStyle)
        return clone

    def ansi(self, ansiCode: str) -> "Color":
        return self._clone(Style(ansiCode))

    def fg16(self, n: int) -> "Color":
        code = u"\x1b[3" + str(n % 8)
        if n > 7:
            code += ";1"
        return self._clone(Style(code + "m"))

    def bg16(self, n: int) -> "Color":
        code = u"\x1b[4" + str(n % 8)
        if n > 7:
            code += ";1"
        return self._clone(Style(code + "m"))

    def fg256(self, n: int) -> "Color":
        return self._clone(Style(u"\x1b[38;5;" + str(n % 256) + "m"))

    def bg256(self, n: int) -> "Color":
        return self._clone(Style(u"\x1b[48;5;" + str(n % 256) + "m"))

    def fgRGB(self, r: int, g: int, b: int) -> "Color":
        return self._clone(Style(u"\x1b[38;2;" + f"{r};{g};{b}m"))

    def bgRGB(self, r: int, g: int, b: int) -> "Color":
        return self._clone(Style(u"\x1b[48;2;" + f"{r};{g};{b}m"))

    # --- TEXT ATTRIBUTES ---

    @property
    def bold(self) -> "Color":
        return self._clone(Style(AnsiStyle.BOLD))

    @property
    def dim(self) -> "Color":
        return self._clone(Style(AnsiStyle.DIM))

    @property
    def italic(self) -> "Color":
        return self._clone(Style(AnsiStyle.ITALIC))

    @property
    def underline(self) -> "Color":
        return self._clone(Style(AnsiStyle.UNDERLINE))

    @property
    def reversed(self) -> "Color":
        return self._clone(Style(AnsiStyle.REVERSED))

    # --- FG8 ---

    @property
    def black(self) -> "Color":
        return self._clone(Style(AnsiStyle.BLACK))

    @property
    def red(self) -> "Color":
        return self._clone(Style(AnsiStyle.RED))

    @property
    def green(self) -> "Color":
        return self._clone(Style(AnsiStyle.GREEN))

    @property
    def yellow(self) -> "Color":
        return self._clone(Style(AnsiStyle.YELLOW))

    @property
    def blue(self) -> "Color":
        return self._clone(Style(AnsiStyle.BLUE))

    @property
    def magenta(self) -> "Color":
        return self._clone(Style(AnsiStyle.MAGENTA))

    @property
    def cyan(self) -> "Color":
        return self._clone(Style(AnsiStyle.CYAN))

    @property
    def white(self) -> "Color":
        return self._clone(Style(AnsiStyle.WHITE))

    # --- FG16 ---

    @property
    def blackBright(self) -> "Color":
        return self._clone(Style(AnsiStyle.BLACK_BRIGHT))

    @property
    def redBright(self) -> "Color":
        return self._clone(Style(AnsiStyle.RED_BRIGHT))

    @property
    def greenBright(self) -> "Color":
        return self._clone(Style(AnsiStyle.GREEN_BRIGHT))

    @property
    def yellowBright(self) -> "Color":
        return self._clone(Style(AnsiStyle.YELLOW_BRIGHT))

    @property
    def blueBright(self) -> "Color":
        return self._clone(Style(AnsiStyle.BLUE_BRIGHT))

    @property
    def magentaBright(self) -> "Color":
        return self._clone(Style(AnsiStyle.MAGENTA_BRIGHT))

    @property
    def cyanBright(self) -> "Color":
        return self._clone(Style(AnsiStyle.CYAN_BRIGHT))

    @property
    def whiteBright(self) -> "Color":
        return self._clone(Style(AnsiStyle.BLACK_BRIGHT))

    # --- BG8 ---

    @property
    def bgBlack(self) -> "Color":
        return self._clone(Style(AnsiStyle.BG_BLACK))

    @property
    def bgRed(self) -> "Color":
        return self._clone(Style(AnsiStyle.BG_RED))

    @property
    def bgGreen(self) -> "Color":
        return self._clone(Style(AnsiStyle.BG_GREEN))

    @property
    def bgYellow(self) -> "Color":
        return self._clone(Style(AnsiStyle.BG_YELLOW))

    @property
    def bgBlue(self) -> "Color":
        return self._clone(Style(AnsiStyle.BG_BLUE))

    @property
    def bgMagenta(self) -> "Color":
        return self._clone(Style(AnsiStyle.BG_MAGENTA))

    @property
    def bgCyan(self) -> "Color":
        return self._clone(Style(AnsiStyle.BG_CYAN))

    @property
    def bgWhite(self) -> "Color":
        return self._clone(Style(AnsiStyle.BG_WHITE))

    # --- BG16 ---

    @property
    def bgBlackBright(self) -> "Color":
        return self._clone(Style(AnsiStyle.BG_BLACK_BRIGHT))

    @property
    def bgRedBright(self) -> "Color":
        return self._clone(Style(AnsiStyle.BG_RED_BRIGHT))

    @property
    def bgGreenBright(self) -> "Color":
        return self._clone(Style(AnsiStyle.BG_GREEN_BRIGHT))

    @property
    def bgYellowBright(self) -> "Color":
        return self._clone(Style(AnsiStyle.BG_YELLOW_BRIGHT))

    @property
    def bgBlueBright(self) -> "Color":
        return self._clone(Style(AnsiStyle.BG_BLUE_BRIGHT))

    @property
    def bgMagentaBright(self) -> "Color":
        return self._clone(Style(AnsiStyle.BG_MAGENTA_BRIGHT))

    @property
    def bgCyanBright(self) -> "Color":
        return self._clone(Style(AnsiStyle.BG_CYAN_BRIGHT))

    @property
    def bgWhiteBright(self) -> "Color":
        return self._clone(Style(AnsiStyle.BG_BLACK_BRIGHT))


color = Color()
