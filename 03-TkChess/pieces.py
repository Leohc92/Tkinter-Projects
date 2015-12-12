"""
Code illustration: 4.07

NO CHANGES FROM PREVIOUS ITERATION

Tkinter GUI Application Development Hotshot
""" 

import sys

SHORT_NAME = {
 'R':'Rook',
 'N':'Knight',
 'B':'Bishop',
 'Q':'Queen',
 'K':'King',
 'P':'Pawn'
}


def create_piece(piece, color='white'):
    ''' Takes a piece name or shortname and returns the corresponding piece instance '''
    if piece in (None, ' '): return
    if len(piece) == 1:
        if piece.isupper(): color = 'white'
        else: color = 'black'
        piece = SHORT_NAME[piece.upper()]
    module = sys.modules[__name__]
    return module.__dict__[piece](color)

class Piece(object):

    def __init__(self, color):
        if color == 'black':
            self.shortname = self.shortname.lower()
        elif color == 'white':
            self.shortname = self.shortname.upper()
        self.color = color

    def place(self, board):
        ''' Keep a reference to the board '''
        self.board = board

    def moves_available(self, pos, orthogonal, diagonal, distance):
        board = self.board
        allowed_moves = []
        orth  = ((-1,0),(0,-1),(0,1),(1,0))
        diag  = ((-1,-1),(-1,1),(1,-1),(1,1))
        piece = self
        beginningpos = board.num_notation(pos.upper())
        if orthogonal and diagonal:
            directions = diag+orth
        elif diagonal:
            directions = diag
        elif orthogonal:
            directions = orth
        for x,y in directions:
            collision = False
            for step in range(1, distance+1):
                if collision: break
                dest = beginningpos[0]+step*x, beginningpos[1]+step*y
                if self.board.alpha_notation(dest) not in board.occupied('white') + board.occupied('black'):
                    allowed_moves.append(dest)
                elif self.board.alpha_notation(dest) in board.occupied(piece.color):
                    collision = True
                else:
                    allowed_moves.append(dest)
                    collision = True
        allowed_moves = filter(board.is_on_board, allowed_moves)
        return map(board.alpha_notation, allowed_moves)



class King(Piece):
    shortname = 'k'
    def moves_available(self,pos):
        return super(King, self).moves_available(pos.upper(), True, True, 1)

class Queen(Piece):
    shortname = 'q'
    def moves_available(self,pos):
        return super(Queen, self).moves_available(pos.upper(), True, True, 8)

class Rook(Piece):
    shortname = 'r'
    def moves_available(self,pos):
        return super(Rook, self).moves_available(pos.upper(), True, False, 8)

class Bishop(Piece):
    shortname = 'b'
    def moves_available(self,pos):
        return super(Bishop,self).moves_available(pos.upper(), False, True, 8)

class Knight(Piece):
    shortname = 'n'
    def moves_available(self,pos):
        board = self.board
        allowed_moves = []
        beginningpos = board.num_notation(pos.upper())
        piece = board.get(pos.upper())
        deltas = ((-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1))
        for x,y in deltas:
            dest = beginningpos[0]+x, beginningpos[1]+y
            if(board.alpha_notation(dest) not in board.occupied(piece.color)):
                allowed_moves.append(dest)
        allowed_moves = filter(board.is_on_board, allowed_moves)
        return map(board.alpha_notation, allowed_moves)


class Pawn(Piece):
    shortname = 'p'
    def moves_available(self, pos):
        board = self.board
        piece = self
        if self.color == 'white':
            startpos, direction, enemy = 1, 1, 'black'
        else:
            startpos, direction, enemy = 6, -1, 'white'
        allowed_moves = []
        # Moving
        prohibited = board.occupied('white') + board.occupied('black')
        beginningpos   = board.num_notation(pos.upper())
        forward = beginningpos[0] + direction, beginningpos[1]
        if board.alpha_notation(forward) not in prohibited:
            allowed_moves.append(forward)
            if beginningpos[0] == startpos:
                # If pawn is in starting position allow double moves
                double_forward = (forward[0] + direction, forward[1])
                if board.alpha_notation(double_forward) not in prohibited:
                    allowed_moves.append(double_forward)
        # Attacking
        for a in range(-1, 2, 2):
            attack = beginningpos[0] + direction, beginningpos[1] + a
            if board.alpha_notation(attack) in board.occupied(enemy):
                allowed_moves.append(attack)
        allowed_moves = filter(board.is_on_board, allowed_moves)
        return map(board.alpha_notation, allowed_moves)


