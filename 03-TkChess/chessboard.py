#coding:utf8

import pieces
import re

START_PATTERN = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w 0 1'

class Board(dict):
	y_axis = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H')
	x_axis = (1, 2, 3, 4, 5, 6, 7, 8)

	def __init__(self, patt = None):
		self.process_notation(START_PATTERN)

	def alpha_notation(self, xycoord):
		# if not self.is_on_board(xycoord):return 
		return self.y_axis[xycoord[1]] + str(self.x_axis[xycoord[0]])

	def num_notation(self, xycoord):
		return int(xycoord[1])-1, self.y_axis.index(xycoord[0])

	def process_notation(self, patt):
		patt = patt.split(' ')
		def expand_whitespaces(match): return ' '*int(match.group(0))
		patt[0] = re.compile(r'\d').sub(expand_whitespaces, patt[0])
		for x, row in enumerate(patt[0].split('/')):
			for y, alphabet in enumerate(row):
				if alphabet == ' ': continue
				xycoord = self.alpha_notation((7-x, y))
				self[xycoord] = pieces.create_piece(alphabet)
				self[xycoord].ref(self)
		if patt[1] == 'w': self.player_turn = 'white'
		else: 
			self.player_turn = 'black'

	def occupied(self, color):
		result=[]
		for coord in self:
			if self[coord].color == color:
				result.append(coord)
			return result

	def is_on_board(self, coord):
		if coord[1]<0 or coord[1]>7 or coord[0]<0 or coord[0]>7:
			return False
		else: return True

class ChessError(Exception): pass