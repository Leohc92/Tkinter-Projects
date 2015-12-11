#coding:utf8

from Tkinter import *
import chessboard
from PIL import ImageTk

class GUI():
	rows = 8
	columns = 8
	color1 = '#DDB88C'
	color2 = '#A66D4F'
	dim_square = 64
	images = {}

	def __init__(self, parent, chessboard):
		self.parent = parent
		self.chessboard = chessboard
		canvas_width = self.columns * self.dim_square
		canvas_height = self.rows * self.dim_square
		self.canvas = Canvas(parent, width=canvas_width, height=canvas_height)
		self.canvas.pack(padx=8, pady=8)

	def draw_board(self):
		for r in range(self.rows):
			for c in range(self.columns):
				color = self.color1 if r%2==c%2 else self.color2
				x1 = c * self.dim_square
				y1 = r * self.dim_square
				x2 = x1 + self.dim_square
				y2 = y1 + self.dim_square
				self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, tags="area")

	def draw_pieces(self):
		self.canvas.delete("occupied")
		for xycoord, piece in self.chessboard.iteritems():
			x,y = self.chessboard.num_notation(xycoord)
			if piece is not None:
				filename = "pieces_image/%s%s.png" % (piece.shortname.lower(), piece.color)
				piecename = "%s%s%s" % (piece.shortname, x, y)
				if (filename not in self.images):
					self.images[filename] = ImageTk.PhotoImage(file=filename)
				self.canvas.create_image(0, 0, image=self.images[filename], tags=(piecename, "occupied"), anchor='c')
				x0 = (y * self.dim_square) + int(self.dim_square/2)
				y0 = ((7-x) * self.dim_square) + int(self.dim_square/2)
				self.canvas.coords(piecename, x0, y0)

def main(chessboard):
	root = Tk()
	root.title('Chess')
	gui = GUI(root, chessboard)
	gui.draw_board()
	gui.draw_pieces()
	root.mainloop()

#################################################
if __name__ == '__main__':
	game = chessboard.Board()
	main(game)