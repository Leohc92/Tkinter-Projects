#coding:utf-8

#A Drum Machine by Tkinter
from Tkinter import *

##################################################
MAX_DRUM_NUM = 5


##################################################
#DrumMachine class
class DrumMachine():
	def create_top_bar(self):
		topbar_frame = Frame(self.root)
		topbar_frame.grid(row=0, column=0, columnspan=12, rowspan=10, padx=5, pady=5)

		Label(topbar_frame, text='Units:').grid(row=0, column=0, padx=2, pady=5)
		self.units = IntVar()
		self.units.set(4)
		self.units_widget = Spinbox(topbar_frame, from_=1, to=8, width=5, textvariable=self.units)
		self.units_widget.grid(row=0, column=1, padx=2, pady=5)

		Label(topbar_frame, text='BPUs:').grid(row=0, column=3, padx=2, pady=5)
		self.bpu = IntVar()
		self.bpu.set(4)
		self.bpu_widget = Spinbox(topbar_frame, from_=1, to=10, width=5, textvariable=self.bpu)
		self.bpu_widget.grid(row=0, column=4, padx=2, pady=5)

	def create_left_pad(self):
		left_frame = Frame(self.root)
		left_frame.grid(row=10, column=0, columnspan=6, padx=10)
		tbicon = PhotoImage(file='images/openfile.gif')
		for i in range(0, MAX_DRUM_NUM):
			button = Button(left_frame, image=tbicon)
			button.image = tbicon
			button.grid(row=i, column=0, padx=5, pady=2)
			self.drum_entry = Entry(left_frame)
			self.drum_entry.grid(row=i, column=1, padx=7, pady=2)

	def create_right_pad(self):
		right_frame = Frame(self.root)
		right_frame.grid(row=10, column=6, padx=10, pady=2)
		self.button = [[0 for x in range(4)] for x in range(MAX_DRUM_NUM)]
		for i in range(MAX_DRUM_NUM):
			for j in range(4):
				self.button[i][j] = Button(right_frame, bg='grey55')
				self.button[i][j].grid(row=i, column=j)

	def create_play_bar(self):
		playbar_frame = Frame(self.root)
		playbar_frame.grid(row=12, column=0,columnspan=13, sticky=W+E, padx=10, pady=5)  ##padx? 
		button = Button(playbar_frame, text='Play')
		button.grid(row=0, column=0, padx=2, pady=2)
		button = Button(playbar_frame, text='Stop')
		button.grid(row=0, column=1, padx=2, pady=2)
		loop = BooleanVar()
		loopbutton = Checkbutton(playbar_frame, text='Loop', variable=loop)
		loopbutton.grid(row=0, column=2, padx=2, pady=2)

	def app(self):
		self.root = Tk()
		self.root.title('Drum Beast')
		self.create_top_bar()
		self.create_left_pad()
		self.create_right_pad()
		self.create_play_bar()
		self.root.mainloop()


###################################################
if __name__ == '__main__':
	dm = DrumMachine()
	dm.app()