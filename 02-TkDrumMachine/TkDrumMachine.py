#coding:utf-8

#A Drum Machine by Tkinter
from Tkinter import *
import ttk
import time
import wave
import pymedia.audio.sound as sound
import tkFileDialog
import tkMessageBox
import threading
import pickle
import os


MAX_DRUM_NUM= 5   

class DrumMachine():

	def __init__(self):
		self.widget_drum_name = []
		self.widget_drum_file_name = [0] * MAX_DRUM_NUM
		self.current_drum_no = 0
		self.keep_playing = True
		self.loop = False
		self.pattern_list = [None]*10


	def save_project(self):
		self.record_pattern()  #to make sure the last pattern is saved
		file_name = tkFileDialog.asksaveasfilename(filetypes=[('Drum Beat File','*.bt')], title="Save project as...")
		pickle.dump(self.pattern_list, open(file_name, "wb"))
		self.root.title(os.path.basename(file_name) + " - Drum Beast")

	def load_project(self):
		file_name = tkFileDialog.askopenfilename(filetypes=[('Drum Beat File','*.bt')], title="Load Project")
		if file_name == '' :return
		self.root.title(os.path.basename(file_name) + " - Drum Beast")
		fh = open(file_name, "rb")
		try:
			while True:
				self.pattern_list = pickle.load(fh)
		except EOFError:
			pass
		fh.close()
		try:
			self.reconstruct_pattern(0, self.pattern_list[0]['bpu'], self.pattern_list[0]['units'])
		except:
			tkMessageBox.showerror("Error", "An unexpected error occurred trying to reconstruct patterns")

	def about(self):
		tkMessageBox.showinfo("About", "Tkinter GUI Application\n Development by Leohc92")

	def exit_app(self):
		if tkMessageBox.askokcancel("Quit", "Do you really want to quit?"):
			self.root.destroy()
#basic UI
	def create_top_menu(self):
		self.menubar = Menu(self.root)

		self.filemenu = Menu(self.menubar, tearoff=0)

		self.filemenu.add_command(label="Load Project", command=self.load_project)
		self.filemenu.add_command(label="Save Project", command=self.save_project)
		self.filemenu.add_separator()
		self.filemenu.add_command(label="Exit", command=self.exit_app)
		self.menubar.add_cascade(label="File", menu=self.filemenu)

		self.aboutmenu = Menu(self.menubar, tearoff=0)
		self.aboutmenu.add_command(label="About", command=self.about)
		self.menubar.add_cascade(label="About", menu=self.aboutmenu)

		self.root.config(menu=self.menubar)

	def create_top_bar(self):
		topbar_frame = Frame(self.root)
		topbar_frame.grid(row=0, column=0, columnspan=12, rowspan=10, padx=5, pady=5, sticky=W+E)
  		#pattern
		Label(topbar_frame, text='Pattern Number:').grid(row=0, column=0)
		self.patt = IntVar()
		self.patt.set(0)
		self.prevpatvalue = 0  #to trace last click
		Spinbox(topbar_frame, from_=0, to=9, width=5, textvariable=self.patt, command=self.record_pattern).grid(row=0, column=1)
		self.pat_name = Entry(topbar_frame)
		self.pat_name.grid(row=0, column=2, padx=7, pady=2)
		self.pat_name.insert(0, 'Pattern %s'%self.patt.get())
		self.pat_name.config(state='readonly')

		#units
		Label(topbar_frame, text='Units:').grid(row=0, column=3, padx=2, pady=5)
		self.units = IntVar()
		self.units.set(4)
		self.units_widget = Spinbox(topbar_frame, from_=1, to=8, width=5, textvariable=self.units, command=self.create_right_pad)
		self.units_widget.grid(row=0, column=4, padx=2, pady=5)

		#bpus
		Label(topbar_frame, text='BPUs:').grid(row=0, column=5, padx=2, pady=5)
		self.bpu = IntVar()
		self.bpu.set(4)
		self.bpu_widget = Spinbox(topbar_frame, from_=1, to=10, width=5, textvariable=self.bpu, command=self.create_right_pad)
		self.bpu_widget.grid(row=0, column=6, padx=2, pady=5)

		self.create_right_pad()

	def record_pattern(self):
		pattern_num, bpu, units = self.patt.get(), self.bpu.get(), self.units.get()
		self.pat_name.config(state='normal')
		self.pat_name.delete(0, END)
		self.pat_name.insert(0, 'Pattern %s'%pattern_num)
		self.pat_name.config(state='readonly')
		prevpval = self.prevpatvalue
		self.prevpatvalue = pattern_num
		c = bpu*units
		self.buttonpickleformat = [[0]* c for x in range(MAX_DRUM_NUM)]
		for i in range(MAX_DRUM_NUM):
			for j  in range(c):
				if self.button[i][j].config('bg')[-1] == 'green':
					self.buttonpickleformat[i][j] = 'active'
		self.pattern_list[prevpval] = {'df':self.widget_drum_file_name, 'bl': self.buttonpickleformat, 'bpu': bpu, 'units':units}
		self.reconstruct_pattern(pattern_num, bpu, units)

	def reconstruct_pattern(self, pattern_num, bpu, units):
		self.widget_drum_file_name = [0]*MAX_DRUM_NUM
		try:
			self.df = self.pattern_list[pattern_num]['df']
			for i in range(len(self.df)):
				file_name = self.df[i]
				if file_name == 0:
					self.widget_drum_name[i].delete(0, END)
					continue
				self.widget_drum_file_name.insert(i, file_name)
				drum_name = os.path.basename(file_name)
				self.widget_drum_name[i].delete(0, END)
				self.widget_drum_name[i].insert(0, drum_name)
		except:
				for i in range(MAX_DRUM_NUM):
					try: self.df
					except: self.widget_drum_name[i].delete(0, END)
		try:
			bpu = self.pattern_list[pattern_num]['bpu']
			units = self.pattern_list[pattern_num]['units']
		except:
			return		
		self.bpu_widget.delete(0, END)
		self.bpu_widget.insert(0, bpu)
		self.units_widget.delete(0, END)
		self.units_widget.insert(0, units)
		self.create_right_pad()
		c = bpu*units
		self.create_right_pad()
		try:
			for i in range(MAX_DRUM_NUM):
				for j in range(c):
					if self.pattern_list[pattern_num]['bl'][i][j] == 'active':
						self.button[i][j].config(bg='green')
		except:return
				


	def create_left_pad(self):
		left_frame = Frame(self.root)
		left_frame.grid(row=10, column=0, columnspan=6, padx=10)
		tbicon = PhotoImage(file='images/openfile.gif')
		for i in range(0, MAX_DRUM_NUM):
			button = Button(left_frame, image=tbicon, command=self.drum_load(i))
			button.image = tbicon
			button.grid(row=i, column=0, padx=5, pady=2)
			self.drum_entry = Entry(left_frame)
			self.drum_entry.grid(row=i, column=1, padx=7, pady=2)
			self.widget_drum_name.append(self.drum_entry)

	def create_right_pad(self):
		bpu = self.bpu.get()
		units = self.units.get()
		c = bpu * units
		self.playlist =[[0]*c for x in range(MAX_DRUM_NUM)]
		right_frame = Frame(self.root)
		right_frame.grid(row=10, column=6, sticky=E+W, padx=10, pady=2)
		self.button = [[0 for x in range(c)] for x in range(MAX_DRUM_NUM)]
		for i in range(MAX_DRUM_NUM):
			for j in range(c):
				color = 'grey55' if (j/bpu)%2 else 'khaki'
				self.button[i][j] = Button(right_frame, bg=color, width=1, command=self.button_clicked(i,j,bpu))
				self.button[i][j].grid(row=i, column=j)

	def button_clicked(self, i, j, bpu):
		def callback():
			btn = self.button[i][j]
			color = 'grey55' if (j/bpu)%2 else 'khaki'
			if btn.cget('bg')=='green':
				new_color = color
				self.playlist[i][j]=0
			else:
				new_color = 'green'
				self.playlist[i][j]=1
			btn.config(bg=new_color)
		return callback


	def create_play_bar(self):
		playbar_frame = Frame(self.root)
		playbar_frame.grid(row=12, column=0,columnspan=13, sticky=W+E, padx=10, pady=5) 
		self.start_button = ttk.Button(playbar_frame, text='Play', command=self.play_in_threading)
		self.start_button.grid(row=0, column=0, padx=2, pady=2)
		button = ttk.Button(playbar_frame, text='Stop', command=self.stop_play)
		button.grid(row=0, column=1, padx=2, pady=2)
		loop = BooleanVar()
		loopbutton = ttk.Checkbutton(playbar_frame, text='Loop', variable=loop, command=lambda:self.loop_play(loop.get()))
		loopbutton.grid(row=0, column=2, padx=2, pady=2)
		photo = PhotoImage(file='images/sig.gif')
		label = Label(playbar_frame, image=photo)
		label.image = photo
		label.grid(row=0, column=3, padx=2, sticky=E)

	def drum_load(self, drum_no):
		def callback():
			self.current_drum_no = drum_no
			try:
				file_name = tkFileDialog.askopenfilename(defaultextension=".wav", filetypes=[("Wave Files","*.wav"),("OGG Files","*.ogg")])
				if not file_name: return
				try:
					del self.widget_drum_file_name[drum_no]
				except:pass
				self.widget_drum_file_name.insert(drum_no, file_name)
				drum_name = os.path.basename(file_name)
				self.widget_drum_name[drum_no].delete(0, END)
				self.widget_drum_name[drum_no].insert(0, drum_name)
			except:
				tkMessageBox.showerror("Invalid", "Error loading drum samples")
		return callback

	def play_sound(self, sound_filename):
		try:
			self.s = wave.open(sound_filename, 'rb')
			sample_rate = self.s.getframerate()
			channels = self.s.getnchannels()
			frmt = sound.AFMT_S16_LE
			self.snd = sound.Output(sample_rate, channels, frmt)
			s = self.s.readframes(300000)
			self.snd.play(s)
		except:
			pass

	def play(self):
		self.keep_playing = True
		while self.keep_playing:
			for c in range(len(self.playlist[0])):
				for r in range(len(self.playlist)):
					try:
						if self.playlist[r][c] == 1:
							if not self.widget_drum_file_name[r]:continue
							sound_filename = self.widget_drum_file_name[r]
							self.play_sound(sound_filename)
					except:
						continue
				time.sleep(1/6.0)
				if self.loop == False: self.keep_playing = False
		self.start_button.config(state='normal')

	def play_in_threading(self):
		self.start_button.config(state='disabled')
		self.thread = threading.Thread(None, self.play, None,(), {})
		self.thread.start()

	def stop_play(self):
		self.keep_playing = False
		self.start_button.config(state='normal')
		return

	def loop_play(self,xval):
		self.loop = xval

	def app(self):
		self.root = Tk()
		self.root.title('Drum Beast')
		self.create_top_menu()
		self.create_top_bar()
		self.create_left_pad()
		self.create_play_bar()
		self.root.protocol('WM_DELETE_WINDOW', self.exit_app)
		self.root.wm_iconbitmap('images/beast.ico')
		self.root.mainloop()

###################################################
if __name__ == '__main__':
	dm = DrumMachine()
	dm.app()

