from color import Color
from figure import Figure
from figure_moving import FigureMoving
from square import Square

__all__ = ()


class Moves:
    def __init__(self, board):
        self.fm = FigureMoving()
        self.board = board

    def can_move(self, fm, dont_check_check=False):
        self.fm = fm
        if dont_check_check:
            return (
                self.can_move_from() and self.can_move_to() and self.can_figure_move()
            )

        return (
            self.can_move_from()
            and self.can_move_to()
            and self.can_figure_move()
            and not self.board.is_check_after(fm)
        )

    def can_move_from(self):
        return (
            self.fm.from_square.on_board()
            and self.fm.figure.get_color() == self.board.move_color_value
            and self.fm.figure == self.board.get_figure_at(self.fm.from_square)
        )

    def can_move_to(self):
        return (
            self.fm.to_square.on_board()
            and self.board.get_figure_at(self.fm.to_square).get_color()
            != self.board.move_color_value
        )

    def can_figure_move(self):
        match self.fm.figure:
            case Figure.white_king | Figure.black_king:
                return self.can_king_move()
            case Figure.white_queen | Figure.black_queen:
                return self.can_queen_move()
            case Figure.white_rook | Figure.black_rook:
                return self.can_rook_move()
            case Figure.white_knight | Figure.black_knight:
                return self.can_knight_move()
            case Figure.white_bishop | Figure.black_bishop:
                return self.can_bishop_move()
            case Figure.white_pawn | Figure.black_pawn:
                return self.can_pawn_move()
        return Figure.none

    def can_king_move(self):
        return self.can_king_literally_move() or self.can_king_castle()

    def can_queen_move(self):
        return self.can_straight_move()

    def can_rook_move(self):
        return (self.fm.sign_x == 0 or self.fm.sign_y == 0) and self.can_straight_move()

    def can_knight_move(self):
        return (self.fm.abs_delta_x == 1 and self.fm.abs_delta_y == 2) or (
            self.fm.abs_delta_x == 2 and self.fm.abs_delta_y == 1
        )

    def can_bishop_move(self):
        return (
            self.fm.sign_x != 0 and self.fm.sign_y != 0
        ) and self.can_straight_move()

    def can_pawn_move(self):
        if self.fm.from_square.y < 1 or self.fm.from_square.y > 6:
            return False

        step_y = 1 if self.fm.figure.get_color() == Color.white else -1
        return (
            self.can_pawn_go(step_y)
            or self.can_pawn_jump(step_y)
            or self.can_pawn_capture(step_y)
            or self.can_pawn_en_passant(step_y)
        )

    def can_king_literally_move(self):
        return (self.fm.abs_delta_x <= 1) and (self.fm.abs_delta_y <= 1)

    def can_king_castle(self):
        if self.fm.figure == Figure.white_king:
            if self.fm.from_square == Square("e1"):
                if self.fm.to_square == Square("g1"):
                    if self.board.can_castle_h1:
                        if self.board.get_figure_at(Square("h1")) == Figure.white_rook:
                            if self.board.get_figure_at(Square("f1")) == Figure.none:
                                if (
                                    self.board.get_figure_at(Square("g1"))
                                    == Figure.none
                                ):
                                    if not self.board.is_check():
                                        if not self.board.is_check_after(
                                            FigureMoving.figure_moving_from_move(
                                                "Ke1f1",
                                            ),
                                        ):
                                            return True
                elif self.fm.to_square == Square("c1"):
                    if self.board.can_castle_a1:
                        if self.board.get_figure_at(Square("a1")) == Figure.white_rook:
                            if self.board.get_figure_at(Square("b1")) == Figure.none:
                                if (
                                    self.board.get_figure_at(Square("c1"))
                                    == Figure.none
                                ):
                                    if (
                                        self.board.get_figure_at(Square("d1"))
                                        == Figure.none
                                    ):
                                        if not self.board.is_check():
                                            if not self.board.is_check_after(
                                                FigureMoving.figure_moving_from_move(
                                                    "Ke1d1",
                                                ),
                                            ):
                                                return True
        elif self.fm.figure == Figure.black_king:
            if self.fm.from_square == Square("e8"):
                if self.fm.to_square == Square("g8"):
                    if self.board.can_castle_h8:
                        if self.board.get_figure_at(Square("h8")) == Figure.black_rook:
                            if self.board.get_figure_at(Square("f8")) == Figure.none:
                                if (
                                    self.board.get_figure_at(Square("g8"))
                                    == Figure.none
                                ):
                                    if not self.board.is_check():
                                        if not self.board.is_check_after(
                                            FigureMoving.figure_moving_from_move(
                                                "ke8f8",
                                            ),
                                        ):
                                            return True
                elif self.fm.to_square == Square("c8"):
                    if self.board.can_castle_a8:
                        if self.board.get_figure_at(Square("a8")) == Figure.black_rook:
                            if self.board.get_figure_at(Square("b8")) == Figure.none:
                                if (
                                    self.board.get_figure_at(Square("c8"))
                                    == Figure.none
                                ):
                                    if (
                                        self.board.get_figure_at(Square("d8"))
                                        == Figure.none
                                    ):
                                        if not self.board.is_check():
                                            if not self.board.is_check_after(
                                                FigureMoving.figure_moving_from_move(
                                                    "ke8c8",
                                                ),
                                            ):
                                                return True

        return False

    def can_straight_move(self):
        at = self.fm.from_square
        flag = True
        while (at.on_board() and self.board.get_figure_at(at) == Figure.none) or flag:
            if flag:
                flag = False

            at = Square.from_x_y(at.x + self.fm.sign_x, at.y + self.fm.sign_y)
            if at == self.fm.to_square:
                return True

        return False

    def can_pawn_go(self, step_y):
        if self.board.get_figure_at(self.fm.to_square) == Figure.none:
            if self.fm.delta_x == 0:
                if self.fm.delta_y == step_y:
                    return True

        return False

    def can_pawn_jump(self, step_y):
        if self.board.get_figure_at(self.fm.to_square) == Figure.none:
            if (self.fm.from_square.y == 1 and step_y == 1) or (
                self.fm.from_square.y == 6 and step_y == -1
            ):
                if self.fm.delta_x == 0:
                    if self.fm.delta_y == step_y * 2:
                        if (
                            self.board.get_figure_at(
                                Square.from_x_y(
                                    self.fm.from_square.x,
                                    self.fm.from_square.y + step_y,
                                ),
                            )
                            == Figure.none
                        ):
                            return True

        return False

    def can_pawn_capture(self, step_y):
        if self.board.get_figure_at(self.fm.to_square) != Figure.none:
            if self.fm.abs_delta_x == 1:
                if self.fm.delta_y == step_y:
                    return True

        return False

    def can_pawn_en_passant(self, step_y):
        if self.fm.to_square == self.board.en_passant:
            if self.board.get_figure_at(self.fm.to_square) == Figure.none:
                if self.fm.delta_y == step_y:
                    if self.fm.abs_delta_x == 1:
                        if (
                            step_y == 1
                            and self.fm.from_square.y == 4
                            or step_y == -1
                            and self.fm.from_square.y == 3
                        ):
                            return True

        return False
