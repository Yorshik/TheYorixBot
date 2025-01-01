from enum import Enum

from color import Color

__all__ = ()


class Figure(Enum):
    none = "."
    white_king = "K"
    white_queen = "Q"
    white_rook = "R"
    white_knight = "N"
    white_bishop = "B"
    white_pawn = "P"
    black_king = "k"
    black_queen = "q"
    black_rook = "r"
    black_knight = "n"
    black_bishop = "b"
    black_pawn = "p"

    def __str__(self):
        return self.value

    @classmethod
    def get_figure_from_str(cls, move):
        match move:
            case "K":
                return cls.white_king
            case "Q":
                return cls.white_queen
            case "R":
                return cls.white_rook
            case "B":
                return cls.white_bishop
            case "N":
                return cls.white_knight
            case "P":
                return cls.white_pawn
            case "k":
                return cls.black_king
            case "q":
                return cls.black_queen
            case "r":
                return cls.black_rook
            case "b":
                return cls.black_bishop
            case "n":
                return cls.black_knight
            case "p":
                return cls.black_pawn
        return cls.none

    def get_color(self):
        match self:
            case (
                Figure.white_king
                | Figure.white_queen
                | Figure.white_rook
                | Figure.white_knight
                | Figure.white_bishop
                | Figure.white_knight
                | Figure.white_pawn
            ):
                return Color.white
            case (
                Figure.black_king
                | Figure.black_queen
                | Figure.black_rook
                | Figure.black_knight
                | Figure.black_bishop
                | Figure.black_knight
                | Figure.black_pawn
            ):
                return Color.black
        return Color.none

    def yield_promotions(self, to):
        if self == Figure.white_pawn and to.y == 7:
            yield Figure.white_queen
            yield Figure.white_rook
            yield Figure.white_knight
            yield Figure.white_bishop
        elif self == Figure.black_pawn and to.y == 0:
            yield Figure.black_queen
            yield Figure.black_rook
            yield Figure.black_knight
            yield Figure.black_bishop
        else:
            yield Figure.none
