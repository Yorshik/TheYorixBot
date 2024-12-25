from enum import Enum
from color import Color


class Figure(Enum):
    none = '.'
    whiteKing = 'K'
    whiteQueen = 'Q'
    whiteRook = 'R'
    whiteKnight = 'N'
    whiteBishop = 'B'
    whitePawn = 'P'
    blackKing = 'k'
    blackQueen = 'q'
    blackRook = 'r'
    blackKnight = 'n'
    blackBishop = 'b'
    blackPawn = 'p'

    def __str__(self):
        return self.value

    @classmethod
    def get_figure_from_str(cls, move):
        match move:
            case "K":
                return cls.whiteKing
            case "Q":
                return cls.whiteQueen
            case "R":
                return cls.whiteRook
            case "B":
                return cls.whiteBishop
            case "N":
                return cls.whiteKnight
            case "P":
                return cls.whitePawn
            case "k":
                return cls.blackKing
            case "q":
                return cls.blackQueen
            case "r":
                return cls.blackRook
            case "b":
                return cls.blackBishop
            case "n":
                return cls.blackKnight
            case "p":
                return cls.blackPawn
            case _:
                return cls.none

    def get_color(self):
        match self:
            case Figure.whiteKing | \
                 Figure.whiteQueen | \
                 Figure.whiteRook | \
                 Figure.whiteKnight | \
                 Figure.whiteBishop | \
                 Figure.whiteKnight | \
                 Figure.whitePawn:
                return Color.white
            case Figure.blackKing | \
                 Figure.blackQueen | \
                 Figure.blackRook | \
                 Figure.blackKnight | \
                 Figure.blackBishop | \
                 Figure.blackKnight | \
                 Figure.blackPawn:
                return Color.black
            case _:
                return Color.none

    def yield_promotions(self, to):
        if self == Figure.whitePawn and to.y == 7:
            yield Figure.whiteQueen
            yield Figure.whiteRook
            yield Figure.whiteKnight
            yield Figure.whiteBishop
        elif self == Figure.blackPawn and to.y == 0:
            yield Figure.blackQueen
            yield Figure.blackRook
            yield Figure.blackKnight
            yield Figure.blackBishop
        else:
            yield Figure.none
