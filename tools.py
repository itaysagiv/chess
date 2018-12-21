
square_size = 100
board_size = 8
fills = ['white', 'green']

W_King = u"\u2654"
W_Queen = u"\u2655"
W_Rook = u"\u2656"
W_Bishop = u"\u2657"
W_Knight = u"\u2658"
W_Pawn = u"\u2659"

B_King = u"\u265A"
B_Queen = u"\u265B"
B_Rook = u"\u265C"
B_Bishop = u"\u265D"
B_Knight = u"\u265E"
B_Pawn = u"\u265F"


def transpose(mat):
    return list(map(list, zip(*mat)))


init_board = [[W_Rook, W_Knight, W_Bishop, W_King, W_Queen, W_Bishop, W_Knight, W_Rook],
              [W_Pawn, W_Pawn, W_Pawn, W_Pawn, W_Pawn, W_Pawn, W_Pawn, W_Pawn]] +\
              [[''] * 8] * 4 +\
              [[B_Pawn, B_Pawn, B_Pawn, B_Pawn, B_Pawn, B_Pawn, B_Pawn, B_Pawn],
               [B_Rook, B_Knight, B_Bishop, B_King, B_Queen, B_Bishop, B_Knight, B_Rook]]
init_board = transpose(init_board)


def get_color_from_name(name):
    if name:
        if ord(name) & 0xF <= 9:
            return 'W'
        else:
            return 'B'
    else:
        return None


class Piece:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.in_play = True

    def get_color(self):
        return self.color

    def move(self, x, y):
        self.x = x
        self.y = y

    def remove(self):
        self.in_play = False


class Pawn(Piece):
    def __init__(self, x, y, color):
        Piece.__init__(self, x, y, color)
        self.first_location = (x, y)
        self.direction = {'B': -1, 'W': 1}[color]

    def get_possible_moves(self, locations):
        moves = []
        # TODO - add en passant option
        # TODO - add option whrn pawn gets to the end turns into a piece of your choice
        # move one ahead
        if not locations[self.x][self.y + self.direction]:
                moves.append((self.x, self.y + self.direction))
                # first move can move to ahead
                if (self.x, self.y) == self.first_location and not locations[self.x][self.y + self.direction]:
                    if not locations[self.x][self.y + 2*self.direction]:
                            moves.append((self.x, self.y + 2*self.direction))
        if self.x != board_size-1 and\
            locations[self.x + 1][self.y + self.direction] and \
            locations[self.x + 1][self.y + self.direction].get_color() != self.color:
                moves.append((self.x + 1, self.y + self.direction))
        if self.x != 0 and \
            locations[self.x - 1][self.y + self.direction] and \
            locations[self.x - 1][self.y + self.direction].get_color() != self.color:
                moves.append((self.x - 1, self.y + self.direction))
        return moves

class Rook(Piece):
    def __init__(self, x, y, color):
        Piece.__init__(self, x, y, color)

    def get_possible_moves(self, locations):
        # TODO - add castling option
        moves = []
        for x in range(self.x + 1, board_size, 1):
            if locations[x][self.y]:
                if locations[x][self.y].get_color() != self.color:
                    moves.append((x, self.y))
                break
            else:
                moves.append((x, self.y))
        for x in range(self.x - 1, -1, -1):
            if locations[x][self.y]:
                if locations[x][self.y].get_color()!= self.color:
                    moves.append((x, self.y))
                break
            else:
                moves.append((x, self.y))
        for y in range(self.y - 1, -1, -1):
            if locations[self.x][y]:
                if locations[self.x][y].get_color() != self.color:
                    moves.append((self.x, y))
                break
            else:
                moves.append((self.x, y))
        for y in range(self.y + 1, board_size, 1):
            if locations[self.x][y]:
                if locations[self.x][y].get_color() != self.color:
                    moves.append((self.x, y))
                break
            else:
                moves.append((self.x, y))
        return moves


class Knight(Piece):
    def __init__(self, x, y, color):
        Piece.__init__(self, x, y, color)


class Bishop(Piece):
    def __init__(self, x, y, color):
        Piece.__init__(self, x, y, color)


class Queen(Piece):
    def __init__(self, x, y, color):
        Piece.__init__(self, x, y, color)


class King(Piece):
    def __init__(self, x, y, color):
        Piece.__init__(self, x, y, color)


def build_piece(name, x, y):
    if name:
        color = get_color_from_name(name)
        val = (ord(name) - 0x2654) % 6
        return [King(x, y, color),
                Queen(x, y, color),
                Rook(x, y, color),
                Bishop(x, y, color),
                Knight(x, y, color),
                Pawn(x, y, color)][val]
    else:
        return None
