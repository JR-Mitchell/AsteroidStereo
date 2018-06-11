from Stereo.Stereo3 import *

import threading
class UI:
	def __init__(self):
		self.c = StereoClient()
		self.c.start()
		sleep(2)
		self.help()
		self.child = threading.Thread(target=self.now_playing())
		self.child.daemon = True
		self.child.start()
		#self.now_playing()()
		self.loop()

	def help(self):
		print("\n\nWelcome to Asteroid v3.0\n[help] for help\n\n[list] to list songs\n[play [id]] to play\n[pause] to pause\n"+
			"[next] to skip\n[setvol [int]] to set volume\n[shuffle] to shuffle\n"+
			"[playlist] to list playlists\n[load [num]] to load playlist"+
			"\n\n[exit] to exit")

	def now_playing(self):
		def _play_loop():
			k = StereoProbe()
			k.start()
			while True:
				sleep(1)
				if k._check():
					k._now_playing()
				if k._time():
					k._update_time()
		return _play_loop

	def loop(self):
		sleep(4)
		try:
			while True:
				inp = raw_input("\n> ")
				if "list" in inp:
					if "playlist" in inp:
						self.c.list_playlists()
					elif 'play' not in inp:
						self.c.list_songs()
				elif "play" in inp:
					try:
						inp = inp.split(" ")[1]
						inp = int(inp)
					except:
						self.c.play()
					else:
						self.c.play(inp)
				elif "pause" in inp:
					self.c.pause()
				elif "next" in inp:
					self.c.next()
					sleep(1)
				elif "load" in inp:
					try:
						inp = inp.split(" ")[1]
						inp = int(inp)
					except:
						print("Need playlist number.")
					else:
						self.c.load_newplaylist(inp)
				elif "setvol" in inp:
					try:
						inp = inp.split(" ")[1]
						inp = int(inp)
					except:
						print("Value required 0-100.")
					else:
						if (0 <= inp) and (inp <= 100):
							self.c.setvol(inp)
						else:
							print("Volume can only be set from 0-100.")
				elif "shuffle" in inp:
					self.c.shuffle()
				elif "help" in inp:
					self.help()
				elif "exit" in inp:
					print("Shutting down...\n")
					sleep(2)
					self.c.end()
					sleep(1)
					exit(0)
		except (KeyboardInterrupt, SystemExit):
			print("Killing...")
			exit(0)


if __name__ == "__main__":
	ui = UI()