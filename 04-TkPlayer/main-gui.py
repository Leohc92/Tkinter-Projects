#coding:utf8
import os

from Tkinter import *
import tkFileDialog
import ttk
import tkMessageBox
import Pmw

import player

class GUI:

	alltracks = []
	indx = 0
	currentTrack = ''
	timer =[0, 0]
	timepattern = '{0:02d}:{1:02d}'
	loopchoices = [("No Loop",1),("Loop Current",2),("Loop All",3)]
	selectedloopchoice = 3

	def __init__(self, player):
		self.player = player
		player.parent = self
		self.root = Tk()
		self.root.title('TkPlayer')
		self.root.iconbitmap('icons/mp.ico')
		self.balloon = Pmw.Balloon(self.root)
		self.create_console_frame()
		self.create_button_frame()
		self.create_list_frame()
		self.create_bottom_frame()
		self.create_context_menu()
		self.root.protocol('WM_DELETE_WINDOW', self.close_player)
		self.root.mainloop()

	def create_console_frame(self):
		cnslfrm = Frame(self.root)
		photo = PhotoImage(file='icons/glassframe.gif')
		self.canvas = Canvas(cnslfrm, width=370, height=90)
		self.canvas.image = photo
		self.canvas.grid(row=1)
		self.console = self.canvas.create_image(0, 10, anchor=NW, image=photo)
		self.clock = self.canvas.create_text(32, 34, anchor=W, fill='#CBE4F6', font="DS-Digital 20", text="00:00")
		self.songname = self.canvas.create_text(115, 37, anchor=W, fill='#9CEDAC', font="Verdana 10", 
			text='\"Currently playing: none[00.00]\"')
		self.progressBar =  ttk.Progressbar(cnslfrm, length=1, mode="determinate")
		self.progressBar.grid(row=2, columnspan=10, sticky=W+E, padx=5)

		cnslfrm.grid(row=0, padx=0, pady=1)

	def create_button_frame(self):
		buttonframe = Frame(self.root)

		previcon = PhotoImage(file='icons/previous.gif')
		prevbtn = Button(buttonframe, image=previcon, borderwidth=0, padx=0, command=self.prev_track)
		prevbtn.image = previcon
		prevbtn.grid(row=0, column=0)
		self.balloon.bind(prevbtn, 'Previous Song')

		rewindicon = PhotoImage(file='icons/rewind.gif')
		rewindbtn = Button(buttonframe, image=rewindicon, borderwidth=0, padx=0, command=self.player.rewind)
		rewindbtn.image = rewindicon
		rewindbtn.grid(row=0, column=1)
		self.balloon.bind(rewindbtn, 'Go Back')

		self.playicon = PhotoImage(file='icons/play.gif')
		self.stopicon = PhotoImage(file='icons/stop.gif')
		self.playbtn = Button(buttonframe, text='play', image=self.playicon, borderwidth=0, padx=0, command=self.toggle_play_pause)
		self.playbtn.image = self.playicon
		self.playbtn.grid(row = 0, column=2)
		self.balloon.bind(self.playbtn, 'Play Song')

		fast_fwdicon = PhotoImage(file='icons/fast_fwd.gif')
		fast_fwdbtn = Button(buttonframe, image=fast_fwdicon, borderwidth=0, padx=0, command=self.player.fast_fwd)
		fast_fwdbtn.image = fast_fwdicon
		fast_fwdbtn.grid(row=0, column=3)
		self.balloon.bind(fast_fwdbtn, 'Fast Forward')

		nexticon = PhotoImage(file='icons/next.gif')
		nextbtn = Button(buttonframe, image=nexticon, borderwidth=0, padx=0, command=self.next_track)
		nextbtn.image = nexticon
		nextbtn.grid(row=0, column=4)
		self.balloon.bind(nextbtn, 'Next Song')

		self.muteicon = PhotoImage(file='icons/mute.gif')
		self.unmuteicon = PhotoImage(file='icons/unmute.gif')
		self.mutebtn = Button(buttonframe, text='unmute', image=self.unmuteicon, borderwidth=0, padx=0, command=self.toggle_mute)
		self.mutebtn.image = self.unmuteicon
		self.mutebtn.grid(row=0, column=5)
		self.balloon.bind(self.mutebtn, 'Mute/Unmute')

		self.volscale = ttk.Scale(buttonframe, from_=0.0, to=1.0, value=0.6, command=self.vol_update)
		self.volscale.grid(row=0, column=6, padx=5)

		buttonframe.grid(row=1, padx=4, pady=5, sticky=W)



	def create_list_frame(self)	:
		list_frame = Frame(self.root)
		self.listbox = Listbox(list_frame, activestyle='none', cursor='hand2',
			                   bg='#1C3D7D', fg='#A0B9E9', selectmode=EXTENDED, width=60, height=10)
		self.listbox.pack(side=LEFT, fill=BOTH, expand=1)
		self.listbox.bind("<Double-Button-1>", self.identify_track_to_play)
		self.listbox.bind("<Button-3>", self.show_context_menu)
		scrollbar = Scrollbar(list_frame)
		scrollbar.pack(side=RIGHT, fill=BOTH)
		self.listbox.config(yscrollcommand=scrollbar.set)
		scrollbar.config(command=self.listbox.yview)
		list_frame.grid(row=2, padx=5)


	def create_bottom_frame(self):
		bottomframe = Frame(self.root)

		add_fileicon = PhotoImage(file='icons/add_file.gif')
		add_filebtn = Button(bottomframe, text='Add File', image=add_fileicon, borderwidth=0, command=self.add_file)
		add_filebtn.image = add_fileicon
		add_filebtn.grid(row=0, column=0)
		self.balloon.bind(add_filebtn, 'Add New File')

		del_selectedicon = PhotoImage(file='icons/del_selected.gif')
		del_selectedbtn = Button(bottomframe, text='Delete', image=del_selectedicon, borderwidth=0, command=self.del_selected)
		del_selectedbtn.image = del_selectedicon
		del_selectedbtn.grid(row=0, column=1)
		self.balloon.bind(del_selectedbtn, 'Delete Selected')

		add_diricon = PhotoImage(file='icons/add_dir.gif')
		add_dirbtn =  Button(bottomframe, text='Add Dir', image=add_diricon, borderwidth=0, command=self.add_dir)
		add_dirbtn.image = add_diricon
		add_dirbtn.grid(row=0, column=2)
		self.balloon.bind(add_dirbtn, 'Add Directory')

		del_allicon = PhotoImage(file='icons/delall.gif')
		del_allbtn = Button(bottomframe, text='Clear All', image=del_allicon, borderwidth=0, command=self.clear_list)
		del_allbtn.image = del_allicon
		del_allbtn.grid(row=0, column=3)
		self.balloon.bind(del_allbtn, 'Clear All')

		self.loopv = IntVar()
		self.loopv.set(3)
		for txt, val in self.loopchoices:
			Radiobutton(bottomframe, text=txt, variable=self.loopv, command=self.set_loop_choice, value=val).grid(row=0, column=4+val, pady=3)

		bottomframe.grid(row=3, padx=5, pady=5, sticky=W)

	def create_context_menu(self):
		self.context_menu = Menu(self.root, tearoff=0)
		self.context_menu.add_command(label="Play", command=self.identify_track_to_play)
		self.context_menu.add_command(label="Delete", command=self.del_selected)

	def show_context_menu(self, event):
		self.context_menu.tk_popup(event.x_root+45, event.y_root+10, 0)

	def toggle_play_pause(self):
		if self.playbtn['text'] == 'play':
			self.playbtn.config(text='stop', image=self.stopicon)
			self.identify_track_to_play()
		elif self.playbtn['text'] == 'stop':
			self.playbtn.config(text='play', image=self.playicon)
			self.player.pause()

	def add_file(self):
		filename = tkFileDialog.askopenfilename(filetypes=[('All supported', '.mp3 .wav .ogg'), ('All files', '*.*')])
		if filename:
			self.listbox.insert(END, filename)
			self.alltracks = list(self.listbox.get(0, END))

	def del_selected(self):
		while len(self.listbox.curselection())>0:
			self.listbox.delete(self.listbox.curselection()[0])
		self.alltracks =list(self.listbox.get(0, END))

	def add_dir(self):
		path = tkFileDialog.askdirectory()
		if path:
			tfileList = []
			for (dirpath, dirnames, filenames) in os.walk(path):
				for tfile in filenames:
					if tfile.endswith(".mp3") or tfile.endswith(".wav") or tfile.endswith("ogg"):
						tfileList.append(dirpath+"/"+tfile)
			for item in tfileList:
				self.listbox.insert(END, item)
			self.alltracks = list(self.listbox.get(0, END))

	def clear_list(self):
		self.listbox.delete(0, END)
		self.alltracks = list(self.listbox.get(0, END))


	def identify_track_to_play(self, event=None):
		try:
			indx = int(self.listbox.curselection()[0])
			if self.listbox.get(indx) == "":
				self.del_selected()
		except:
			indx = 0
		self.currentTrack = self.listbox.get(indx)
		self.launch_play()

	def launch_play(self):
		try:
			self.player.pause()
		except:
			pass
		self.player.start_play_thread()
		song_lenminute = str(int(self.player.song_length/60))
		song_lensecond = str(int(self.player.song_length%60))

		filename = self.currentTrack.split('/')[-1] + '\n [' + song_lenminute + ':' + song_lensecond + ']'
		self.canvas.itemconfig(self.songname, text=filename)
		self.progressBar["maximum"] = self.player.song_length
		self.update_clock_and_progressbar()

	def update_clock_and_progressbar(self):
		current_time = self.player.current_time()
		song_len = self.player.song_len()
		currtimemin = int(current_time/60)
		currtimesec = int(current_time%60)
		currtimestrng  = self.timepattern.format(currtimemin, currtimesec)
		self.canvas.itemconfig(self.clock, text = currtimestrng)
		self.progressBar["value"] = current_time
		self.root.update()
		if current_time == song_len:
			self.canvas.itemconfig(self.clock, text='00:00')
			self.timer =[0,0]
			self.progressBar["value"] = 0
		else:
			self.canvas.after(1000, self.update_clock_and_progressbar)

	def vol_update(self, e):
		vol = float(e)
		self.player.set_vol(vol)

	def prev_track(self):
		try:
			self.player.pause()
			previndex = self.alltracks.index(self.currentTrack) - 1
			self.currentTrack = self.alltracks[previndex]
		except:
			return
		self.player.start_play_thread()

	def next_track(self):
		try:
			self.player.pause()
			nextindex = self.alltracks.index(self.currentTrack) + 1
			self.currentTrack = self.alltracks[nextindex]
		except:
			return
		self.player.start_play_thread()

	def toggle_mute(self):
		if self.mutebtn.config('text')[-1] == 'unmute':
			print self.mutebtn.config('text')
			self.mutebtn.config(text='mute', image=self.muteicon)
			self.player.mute()
		elif self.mutebtn.config('text')[-1] == 'mute':
			print self.mutebtn.config('text')
			self.mutebtn.config(text='unmute', image=self.unmuteicon)
			self.player.unmute()

	def set_loop_choice(self):
		self.selectedloopchoice = self.loopv.get()

	def close_player(self):
		if tkMessageBox.askokcancel("Quit", "Do you really want to close quit?"):
			try:
				self.player.pause()
			except:
				pass
			self.root.destroy()

if __name__ == '__main__':
	playerobj = player.Player()
	app = GUI(playerobj)