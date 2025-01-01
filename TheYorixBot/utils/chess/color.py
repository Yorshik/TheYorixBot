from enum import Enum

__all__ = ()


class Color(Enum):
    none = ""
    white = "w"
    black = "b"

    @staticmethod
    def flip_color(color):
        if color == Color.black:
            return color.white

        if color == Color.white:
            return color.black

        return Color.none
