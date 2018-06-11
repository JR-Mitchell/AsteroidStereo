
class PlaylistSurgeon:
	def __init__(self, mpd_client):
		self.client = mpd_client
		self.cache = []

	def hold(self, songs):
		self.cache += songs
		if self.client.current_playlist == "Asteroid":
			for i in songs:
				self.client.c.add(str(i))

	def _prepare(self):
		self.client.c.load("Asteroid")
		self.client.current_playlist = "Asteroid"
		self.client.c.clear()

	def _cut(self):
		for song in self.cache:
			try:
				self.client.c.add(str(song))
			except:
				pass

	def _stitch(self):
		self.client.c.play()

	def __call__(self, play=True):
		if len(self.cache) > 0:
			self._prepare()
			self._cut()
			if play: self._stitch()

