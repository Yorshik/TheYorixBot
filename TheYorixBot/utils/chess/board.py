from figure import Figure
from figure_moving import FigureMoving
from square import Square
from moves import Moves
from color import Color
from figure_on_square import FigureOnSquare


class Board:
    def __init__(self, fen):
        self.move_color_value = Color.none
        self.can_castle_a1 = None
        self.can_castle_h1 = None
        self.can_castle_a8 = None
        self.can_castle_h8 = None
        self.en_passant = Square.none
        self.draw_number_value = None
        self.move_number_value = None
        self.figures = [[Figure.none for _ in range(8)] for _ in range(8)]

        self.fen = fen
        self.init()

    def init(self):
        parts = self.fen.split()
        self.init_figures(parts[0])
        self.init_move_color(parts[1])
        self.init_castle_flags(parts[2])
        self.init_en_passant(parts[3])
        self.init_draw_number(parts[4])
        self.init_move_number(parts[5])

    def init_figures(self, item: str):
        for j in range(8, 1, -1):
            item = item.replace(str(j), str(j - 1) + "1")
        item = item.replace("1", Figure.none.value)
        lines = item.split("/")
        for y in range(7, -1, -1):
            for x in range(8):
                self.figures[x][y] = Figure.get_figure_from_str(lines[7 - y][x])

    def init_move_color(self, item):
        self.move_color_value = Color.white if item == 'w' else Color.black

    def init_castle_flags(self, item: str):
        self.can_castle_a1 = "Q" in item
        self.can_castle_h1 = "K" in item
        self.can_castle_a8 = "q" in item
        self.can_castle_h8 = "k" in item

    def init_en_passant(self, item):
        self.en_passant = Square(item)

    def init_draw_number(self, item):
        self.draw_number_value = int(item)

    def init_move_number(self, item):
        self.move_number_value = int(item)

    def move(self, fm):
        return NextBoard(self.fen, fm)

    def get_figure_at(self, square):
        if square.on_board():
            return self.figures[square.x][square.y]
        return Figure.none

    def yield_figure_on_squares(self):
        for square in Square.yield_board_squares():
            if self.get_figure_at(square).get_color() == self.move_color_value:
                yield FigureOnSquare(self.get_figure_at(square), square)

    def is_check_after(self, fm):
        after = self.move(fm)
        return after.can_eat_king()

    def is_check(self):
        return self.is_check_after(FigureMoving.none)

    def can_eat_king(self):
        bad_king = self.find_bad_king()
        moves = Moves(self)
        for fs in self.yield_figure_on_squares():
            if moves.can_move(FigureMoving.figure_moving_from_data(fs, bad_king), dont_check_check=True):
                return True
        return False

    def find_bad_king(self):
        king = Figure.whiteKing if self.move_color_value == Color.black else Figure.blackKing
        for square in Square.yield_board_squares():
            if self.get_figure_at(square) == king:
                return square
        return Square.none


class NextBoard(Board):
    def __init__(self, fen, fm):
        super().__init__(fen)
        self.fm = fm
        self.move_figures()
        self.drop_en_passant()
        self.set_en_passant()
        self.move_castle_rook()
        self.move_number()
        self.move_color()
        self.update_castle_flags()
        self.generateFEN()

    def set_figure_at(self, square, figure):
        if square.on_board():
            self.figures[square.x][square.y] = figure

    def move_figures(self):
        self.set_figure_at(self.fm.from_square, Figure.none)
        self.set_figure_at(self.fm.to_square, self.fm.placed_figure)

    def drop_en_passant(self):
        if self.fm.to_square == self.en_passant:
            if self.fm.figure == Figure.whitePawn or self.fm.figure == Figure.blackPawn:
                self.set_figure_at(Square.from_x_y(self.fm.to_square.x, self.fm.from_square.y), Figure.none)

    def set_en_passant(self):
        self.en_passant = Square.none
        if self.fm.figure == Figure.whitePawn:
            if self.fm.from_square.y == 1 and self.fm.to_square.y == 3:
                self.en_passant = Square.from_x_y(self.fm.from_square.x, 2)
        elif self.fm.figure == Figure.blackPawn:
            if self.fm.from_square.y == 6 and self.fm.to_square.y == 4:
                self.en_passant = Square.from_x_y(self.fm.from_square.x, 5)

    def move_castle_rook(self):
        if self.fm.figure == Figure.whiteKing:
            if self.fm.from_square == Square("e1"):
                if self.fm.to_square == Square("g1"):
                    self.set_figure_at(Square("h1"), Figure.none)
                    self.set_figure_at(Square("f1"), Figure.whiteRook)
                elif self.fm.to_square == Square("c1"):
                    self.set_figure_at(Square("a1"), Figure.none)
                    self.set_figure_at(Square("d1"), Figure.whiteRook)
        elif self.fm.figure == Figure.blackKing:
            if self.fm.from_square == Square("e8"):
                if self.fm.to_square == Square("g8"):
                    self.set_figure_at(Square("h8"), Figure.none)
                    self.set_figure_at(Square("f8"), Figure.blackRook)
                elif self.fm.to_square == Square("c8"):
                    self.set_figure_at(Square("a8"), Figure.none)
                    self.set_figure_at(Square("d8"), Figure.blackRook)

    def move_number(self):
        if self.move_color_value == Color.black:
            self.move_number_value += 1

    def move_color(self):
        self.move_color_value = Color.flip_color(self.move_color_value)

    def update_castle_flags(self):
        match self.fm.figure:
            case Figure.whiteKing:
                self.can_castle_a1 = False
                self.can_castle_h1 = False
            case Figure.whiteRook:
                if self.fm.from_square == Square("a1"):
                    self.can_castle_a1 = False
                elif self.fm.from_square == Square("h1"):
                    self.can_castle_h1 = False
            case Figure.blackKing:
                self.can_castle_a8 = False
                self.can_castle_h8 = False
            case Figure.blackRook:
                if self.fm.from_square == Square("a8"):
                    self.can_castle_a8 = False
                elif self.fm.from_square == Square("h8"):
                    self.can_castle_h8 = False

    def generateFEN(self):
        self.fen = (f'{self.fen_figures()} {self.fen_move_color()} {self.fen_castle_flags()} {self.fen_en_passant()} '
                    f'{self.fen_draw_number()} {self.fen_move_number()}')

    def fen_figures(self):
        figures = ''
        for y in range(7, -1, -1):
            for x in range(8):
                figures += '1' if self.figures[x][y] == Figure.none else str(self.figures[x][y])
            if y > 0:
                figures += '/'
        eight = '11111111'
        for j in range(8, 1, -1):
            figures = figures.replace(eight[:j], str(j))
        return figures

    def fen_move_color(self):
        return self.move_color_value.value

    def fen_castle_flags(self):
        flags = (
            ("Q" if self.can_castle_a1 else "") +
            ("K" if self.can_castle_h1 else "") +
            ("q" if self.can_castle_a8 else "") +
            ("k" if self.can_castle_h8 else "")
        )
        return flags if flags else '-'

    def fen_en_passant(self):
        return self.en_passant.name

    def fen_draw_number(self):
        return str(self.draw_number_value)

    def fen_move_number(self):
        return str(self.move_number_value)
