__all__ = ()


class Square:
    none = None

    def __init__(self, name):
        if (
            len(name) == 2
            and ord("h") >= ord(name[0]) >= ord("a")
            and 8 >= int(name[1]) >= 1
        ):
            self.x = ord(name[0]) - ord("a")
            self.y = int(name[1]) - 1
        else:
            self.x = -1
            self.y = -1

    def __eq__(self, other):
        if not isinstance(other, Square):
            return False

        return (self.x == other.x) and (self.y == other.y)

    def __ne__(self, other):
        return self != other

    @property
    def name(self):
        if self.on_board():
            return chr(ord("a") + self.x) + str(1 + self.y)

        return "-"

    @classmethod
    def from_x_y(cls, x, y):
        return cls(chr(x + ord("a")) + str(y + 1))

    @staticmethod
    def yield_board_squares():
        for y in range(8):
            for x in range(8):
                yield Square.from_x_y(x, y)

    def on_board(self):
        return (0 <= self.x < 8) and (0 <= self.y < 8)


Square.none = Square.from_x_y(-1, -1)
