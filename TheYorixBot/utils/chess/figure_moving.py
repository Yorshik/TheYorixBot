from figure import Figure
from square import Square

__all__ = ()


class FigureMoving:
    none = None

    def __init__(self):
        self.figure = Figure.none
        self.from_square = Square.none
        self.to_square = Square.none
        self.promotion = Figure.none

    def __str__(self):
        return (
            str(self.figure)
            + self.from_square.name
            + self.to_square.name
            + ("" if self.promotion == Figure.none else str(self.promotion))
        )

    @property
    def delta_x(self):
        return self.to_square.x - self.from_square.x

    @property
    def delta_y(self):
        return self.to_square.y - self.from_square.y

    @property
    def abs_delta_x(self):
        return abs(self.delta_x)

    @property
    def abs_delta_y(self):
        return abs(self.delta_y)

    @property
    def sign_x(self):
        if self.delta_x > 0:
            return 1

        if self.delta_y < 0:
            return -1

        return 0

    @property
    def sign_y(self):
        if self.delta_y > 0:
            return 1

        if self.delta_y < 0:
            return -1

        return 0

    @property
    def placed_figure(self):
        return self.figure if self.promotion == Figure.none else self.promotion

    @classmethod
    def figure_moving_from_data(cls, fs, to_square, promotion=Figure.none):
        self = cls()
        self.figure = fs.figure
        self.from_square = fs.square
        self.to_square = to_square
        self.promotion = promotion
        return self

    @classmethod
    def figure_moving_from_move(cls, move):
        self = cls()
        self.figure = Figure.get_figure_from_str(move[0])
        self.from_square = Square(move[1:3])
        self.to_square = Square(move[3:5])
        self.promotion = Figure.none
        if len(move) == 6:
            self.promotion = Figure.get_figure_from_str(move[5])

        return self


FigureMoving.none = FigureMoving()
