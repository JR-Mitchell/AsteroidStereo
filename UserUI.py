from UI import *

class UserUI(UI):
	def now_playing(self):
		def _play_loop():
			k = UserProbe()
			k.start()
			while True:
				sleep(1)
				if k._check():
					k._now_playing()
		return _play_loop

if __name__ == "__main__":
	ui = UserUI()