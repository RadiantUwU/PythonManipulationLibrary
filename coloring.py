from typing import Tuple, Union


class TerminalColors:
    magenta = '\033[95m'
    blue = '\033[94m'
    cyan = '\033[96m'
    green = '\033[92m'
    yellow = '\033[93m'
    red = '\033[91m'
    reset = '\033[0m'
    bold = '\033[1m'
    underline = '\033[4m'
    colors = ['\033[0m', '\033[94m', '\033[92m', '\033[96m', '\033[91m', '\033[95m', '\033[93m', '\033[0m\033[1m']
    types = ['\033[0m', '\033[1m', '\033[4m', '\033[1m\033[4m']
    colortest = ""
    typetest = ""
    for i in range(len(colors)):
        colortest += colors[i]
        colortest += str(i)
    colortest += types[0]
    for i in range(len(types)):
        typetest += types[i]
        typetest += str(i)
        typetest += types[0]

    @staticmethod
    def rgbcolor(r: int, g: int, b: int, isfg: bool = True):
        return f"\x1b[{('38' if isfg else '48')};2;{str(r)};{str(g)};{str(b)}m"


def print_color(string: str, color: int = 0, the_type: int = 0, end: str = "\n") -> None:
    """Prints colorful!
    String: string to be printed
    Color(default 0): Color, for more info, do TerminalColors.colortest
    Type(default 0): Type, for more info, do TerminalColors.typetest
    End(default \\n): End of print"""
    print(
        TerminalColors.reset + TerminalColors.types[the_type % TerminalColors.types.__len__()] + TerminalColors.colors[
            color % TerminalColors.colors.__len__()] + string + TerminalColors.reset, end=end)


# noinspection SpellCheckingInspection
def print_rainbow(string: str, the_type: int = 0, end: str = "\n") -> None:
    """Prints text in rainbow!
    String: string to be printed
    Type(default 0): Type, for more info, do TerminalColors.typetest
    End(default \\n): End of print"""
    print(rainbowify(string, the_type), end=end)


def colorify_high(string: str, fg_color: Tuple[int, int, int], the_type: int = 0,
                  bg_color: Tuple[int, int, int] = None):
    """Colors string with 24-bit RGB values,
    > colorify_high(string,(fg_r,fg_g,fg_b)[,type,(bg_r,bg_g,bg_r)])

    where type is a number
    0b00
    0th bit is bold
    1st bit is underline"""
    assert len(fg_color) == 3
    if bg_color is None:
        return TerminalColors.types[the_type % 4] + TerminalColors.rgbcolor(*fg_color) + string + TerminalColors.reset
    else:
        assert len(bg_color) == 3
        return TerminalColors.types[the_type % 4] + TerminalColors.rgbcolor(*fg_color) + TerminalColors.rgbcolor(
            *bg_color,
            False) + string + TerminalColors.reset


def rainbowify(string: str, the_type: int = 0) -> str:
    """Makes a string rainbow, makes it rainbow when printed."""
    new_str = TerminalColors.types[the_type % 4]
    i = 0
    rainbow = (
        TerminalColors.red, TerminalColors.yellow, TerminalColors.green, TerminalColors.cyan, TerminalColors.blue,
        TerminalColors.magenta)
    for c in string:
        new_str += rainbow[i] + c
        i += 1
        i %= 6
    return new_str + TerminalColors.reset


def colorify(string: str, color: int = 0, the_type: int = 0):
    """Makes a string colorful!"""
    return TerminalColors.reset + TerminalColors.types[the_type % TerminalColors.types.__len__()] + \
           TerminalColors.colors[color % TerminalColors.colors.__len__()] + string + TerminalColors.reset


def print_a_rainbow(splits: int = 1):
    string = ""
    splits *= 2
    i = 0.0
    try:
        while i != 360:
            # noinspection PyTypeChecker
            x: Tuple[int, int, int] = tuple(int(i) for i in hsv_to_rgb((i % 360, 1.0, 1.0)))
            i += (90.0 / splits)
            # noinspection PyTypeChecker
            y: Tuple[int, int, int] = tuple(int(i) for i in hsv_to_rgb((i % 360, 1.0, 1.0)))
            string += colorify_high("▐", y, 0, x)
            i += (90.0 / splits)
            if i > 360:
                break
    except KeyboardInterrupt:
        pass
    return string


def hsv_to_rgb(hsv: Tuple[Union[int, float], Union[int, float], Union[int, float]]) -> Tuple[int, int, int]:
    hsv = (hsv[0] % 360, *hsv[1:3])
    c = hsv[2] * hsv[1]
    x = c * (1 - abs((hsv[0] / 60) % 2 - 1))
    m = hsv[2] - c
    switch = {
        0 <= hsv[0] < 60: (c, x, 0),
        60 <= hsv[0] < 120: (x, c, 0),
        120 <= hsv[0] < 180: (0, c, x),
        180 <= hsv[0] < 240: (0, x, c),
        240 <= hsv[0] < 300: (x, 0, c),
        300 <= hsv[0] < 360: (c, 0, x)
    }
    x = switch[True]
    return (x[0] + m) * 255, (x[1] + m) * 255, (x[2] + m) * 255
