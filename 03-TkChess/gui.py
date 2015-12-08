#coding:utf8

from Tkinter import *

class GUI():
	rows = 8
	columns = 8
	color1 = '#DDB88C'
	color2 = '#A66D4F'
	dim_square = 64

	def __init__(self, parent):
		self.parent = parent
		canvas_width = self.columns * self.dim_square
		canvas_height = self.rows * self.dim_square
		self.canvas = Canvas(parent, width=canvas_width, height=canvas_height)
		self.canvas.pack(padx=8, pady=8)
		self.draw_board()

	def draw_board(self):
		for r in range(self.rows):
			for c in range(self.columns):
				color = self.color1 if r%2==c%2 else self.color2
				x1 = c * self.dim_square
				y1 = r * self.dim_square
				x2 = x1 + self.dim_square
				y2 = y1 + self.dim_square
				self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, tags="area")

def main():
	root = Tk()
	root.title('Chess')
	gui = GUI(root)
	gui.draw_board()
	root.mainloop()

#################################################
if __name__ == '__main__':
	main()