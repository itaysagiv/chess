
from tkinter import *
import tkinter.font as font
#import tkFont
from tools import *


class Player:

    def __init__(self):
        self.pieces = []


class Chess:

    def __init__(self):
        self.root = Tk()
        self.w = Canvas(self.root, width=board_size*square_size, height=board_size*square_size)
        self.w.bind("<Button-1>", self.click_event)
        self.w.pack()
        self.squares = [[None for _ in range(board_size)] for __ in range(board_size)]
        self.locations = [[None for _ in range(board_size)] for __ in range(board_size)]
        self.tools = [[None for _ in range(board_size)] for __ in range(board_size)]
        self.last_move = {'rec': None, 'color': None, 'tool': None, 'location': None}
        self.marked_moves = []
        self.just_moved = True

    def create_board(self):
        # --------------------
        # TODO:
        # fix order of rows and columns in creation and in accessing
        # maybe a different class for representation of movement
        # -------------------
        for row in range(board_size):
            for col in range(board_size):
                s = self.w.create_rectangle(row * square_size,
                                            col * square_size,
                                            (row + 1) * square_size,
                                            (col + 1) * square_size,
                                            fill=fills[(col + row) % 2])
                l = self.w.create_text((row + 0.5) * square_size,
                                       (col + 0.5) * square_size,
                                       fill='black',
                                       font=font.Font(size=70),
                                       text=init_board[row][col])
                self.squares[row][col] = s
                self.locations[row][col] = l
                self.tools[row][col] = build_piece(init_board[row][col], row, col)

    def click_event(self, ev):
        ev_x = int(ev.x/square_size)
        ev_y = int(ev.y/square_size)

        # if the player can choose a move
        if self.squares[ev_x][ev_y] in [elem['rec'] for elem in self.marked_moves] and not self.just_moved:
            self.last_move['tool'].move(ev_x, ev_y)
            self.tools[ev_x][ev_y], self.last_move['tool'] = self.last_move['tool'], None
            self.w.itemconfig(self.squares[ev_x][ev_y], fill='pink')
            self.w.itemconfig(self.locations[ev_x][ev_y], text=self.w.itemcget(self.last_move['location'], 'text'))
            self.w.itemconfig(self.last_move['location'], text='')
            self.just_moved = True
        else:
            self.just_moved = False
            # remove red mark from previous selected square
            if self.last_move['rec']:
                self.w.itemconfig(self.last_move['rec'], fill=self.last_move['color'])

            # remove yellow mark from possible moves
            for move in self.marked_moves:
                self.w.itemconfig(move['rec'], fill=move['color'])
            self.marked_moves = []

            # mark selected square in red
            self.last_move['rec'] = self.squares[ev_x][ev_y]
            self.last_move['color'] = self.w.itemcget(self.last_move['rec'], 'fill')
            self.last_move['tool'] = self.tools[ev_x][ev_y]
            self.last_move['location'] = self.locations[ev_x][ev_y]
            self.w.itemconfig(self.last_move['rec'], fill='red')

            # paint in yellow the possible moves
            if self.last_move['tool']:
                for (x, y) in self.last_move['tool'].get_possible_moves(self.tools):
                    self.marked_moves.append({'rec': self.squares[x][y],
                                              'color': self.w.itemcget(self.squares[x][y], 'fill')})
                    self.w.itemconfig(self.squares[x][y], fill='yellow')




if __name__ == "__main__":

    c = Chess()
    c.create_board()

    mainloop()
