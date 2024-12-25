from board import Board
from moves import Moves
from figure_moving import FigureMoving
from figure import Figure
from square import Square


class Chess:
    def __init__(self, fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"):
        self.is_check = None
        self.is_checkmate = None
        self.is_stalemate = None

        self.board = Board(fen)
        self.moves = Moves(self.board)
        self.set_check_flags()

    @property
    def fen(self):
        return self.board.fen

    @classmethod
    def chess_from_board(cls, board):
        self = cls(board.fen)
        self.board = board
        self.is_check = None
        self.is_checkmate = None
        self.is_stalemate = None

        self.moves = Moves(board)
        self.set_check_flags()
        return self

    def Move(self, move):
        fm = FigureMoving.figure_moving_from_move(move)
        if not self.moves.can_move(fm):
            return self
        next_board = self.board.move(fm)
        for i, row in enumerate(next_board.figures):
            if row[0] == Figure.blackPawn:
                next_board.figures[i][0] = Figure.blackQueen
            if row[-1] == Figure.whitePawn:
                next_board.figures[i][-1] = Figure.whiteQueen
        next_chess = Chess.chess_from_board(next_board)
        return next_chess

    def set_check_flags(self):
        self.is_check = self.board.is_check()
        self.is_checkmate = False
        self.is_stalemate = False
        for _ in self.yield_valid_moves():
            return
        if self.is_check:
            self.is_checkmate = True
        else:
            self.is_stalemate = True

    def get_figure_at(self, x, y):
        square = Square.from_x_y(x, y)
        figure = self.board.get_figure_at(square)
        return figure

    def yield_valid_moves(self):
        for fs in self.board.yield_figure_on_squares():
            for to in Square.yield_board_squares():
                for promotion in fs.figure.yield_promotions(to):
                    fm = FigureMoving.figure_moving_from_data(fs, to, promotion)
                    if self.moves.can_move(fm):
                        if not self.board.is_check_after(fm):
                            yield str(fm)
