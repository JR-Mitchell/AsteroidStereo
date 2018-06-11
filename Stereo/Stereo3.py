from mpd import MPDClient
from time import sleep
from platform import platform
if platform() == "Darwin-17.6.0-x86_64-i386-64bit":
	IP_ADR = "192.168.0.16"
else:
	IP_ADR = "localhost"
PORT = 7890

class StereoLogic():
	def __init__(self):
		pass

	plcache = {}
	def _make_cache(self):
		pl = self.c.listplaylists()
		n = 1
		for i in pl:
			self.plcache[n] = i["playlist"]
			n+=1
		self.metadat = self.c.playlistinfo()

	def _connect(self):
		if self.okay == False:
			self.c = MPDClient()
			try:
				self.c.connect(self.addr, self.port)
			except:
				print("Failed to connect to Mopidy Server @", self.addr, self. port)
				exit(1)
		else:
			exit(1)

class StereoQuery():
	def __init__(self, mpd_client):
		self.mpd_client = mpd_client.c

	def _search(self, stype, string):
		return self.mpd_client.find(stype, string)

	def _find_artist(self, artist):
		art = self._search("artist", artist)
		ret = []
		for i in art:
			if "Album:" not in i['title']:
				ret.append(i)
		return ret

	def _find_album(self, album):
		return self._search("album", album)

	def _find_song(self, title):
		return self._search("title", title)

	def _find_artist_album(self, artist, album):
		alb = self._find_album(album)
		ret = []
		for i in alb:
			if artist.lower() in i["artist"].lower():
				ret.append(i)
		return ret

	def _find_artist_song(self, artist, song):
		art = self._find_artist(artist)
		ret = []
		son = []
		for i in art:
			if artist.lower() in i["artist"].lower():
				if song.lower() in i["title"].lower():
					son.append(i)
				ret.append(i)
		if len(son) >= 1:
			return son
		if len(ret) >= 1:
			return ret
		else:
			return art

	def _find_album_song(self, album, song):
		alb = self._find_album(album)
		ret = []
		for i in alb:
			if album.lower() in i["album"].lower() and song.lower() in i["title"].lower():
				ret.append(i)
		return ret

	def _find_artist_album_song(self, artist, album, song):
		songs = self._find_song(song)
		ret = []
		for i in songs:
			if artist.lower() in i["artist"].lower and album.lower() in i["album"].lower():
				ret.append(i)
		return ret

	def find(self, artist="", album="", song=""):
		print("DEBUG artist = {} album = {} song = {}".format(artist, album, song))
		if album != "" and artist != "" and song != "":
			return self._find_artist_album_song(artist, album, song)
		# no album
		elif album == "" and (artist != "" or song != ""):
			print("DEBUG for Artist, Song")
			if song == "":
				return self._find_artist(artist)
			elif artist == "":
				return self._find_song(song)
			else: return self._find_artist_song(artist, song)
		# no song
		elif song == "" and (artist != "" or album != ""):
			if artist == "":
				return self._find_album(album)
			elif album == "":
				return self._find_artist(artist)
			else:
				return self._find_artist_album(artist, album)
		else:
			return []

class PlayListBuilder():
	def __init__(self, mpd_client, playlist_name):
		self.mpd_client = mpd_client
		self.pname = playlist_name


import serial
class LCDControl():
	path = "/dev/ttyACM0"
	def _write(self, s):
		s = s + "\r"
		self.ser.write(bytes(s))

	def open_serial(self):
		self.ser = serial.Serial(self.path, 9600, timeout=10)
		sleep(2)

class StereoClient(StereoLogic):
	addr = IP_ADR
	port = PORT
	name = "La Belle Dame Sans Merci"
	okay = False
	current_playlist = "None"
	def __init__(self):
		pass

	def start(self):
		self._connect()
		self._make_cache()

	def _load_playlist(self):
		if int(self.c.status()["playlistlength"]) > 400:
			return 0
		try:
			self.c.load(self.name)
		except:
			print("Connection error, retrying...")
			self._connect()
			sleep(1)

	def list_songs(self):
		self._make_cache()
		NMAX = 5
		n = 0
		for i in self.metadat:
			print("Artist:\t%s\nAlbum:\t%s\nSong:\t%s\nID:\t%s\n" %(i["artist"], i["album"], i["title"], i["id"]))
			n += 1
			if n == NMAX:
				n = 0
				if raw_input("[Any key to continue, Q to break]\n").lower() == "q":
					return None

	def play(self, *args):
		if not len(args) > 0:
			self.c.play()
		else:
			self.c.playid(args[0])

	def end(self):
		self.c.disconnect()

	def list_playlists(self):
		self._make_cache()
		pl = self.plcache
		NMAX = 20
		n = 0
		for i, name in pl.items():
			print("Playlist:  #%d\t'%s'" %(i, name))
			n += 1
			if n == NMAX:
				n = 0
				if raw_input("[Any key to continue, Q to break]\n").lower() == "q":
					return None

	def load_newplaylist(self, num):
		try:
			name = self.plcache[num]
		except KeyError:
			print("Playlist #%d does not exist." %(num))
		else:
			print("Clearing current playlist...")
			self.c.clear()
			print("Loading '%s' into cache..." %(name))
			self.c.load(name)
			self.current_playlist = name
			print("Done.\n")

	def pause(self):
		self.c.pause()

	def setvol(self, i):
		self.c.setvol(i)

	def next(self):
		self.c.next()

	_rand = 0
	def shuffle(self):
		if self._rand == 0:
			self._rand = 1
			print("Shuffle: On")
		elif self._rand == 1:
			self._rand = 0
			print("Shuffle: Off")
		self.c.random(self._rand)

import datetime as dt
class UserProbe(StereoLogic):
	addr = IP_ADR
	port = PORT
	okay = False
	def __init__(self):
		pass

	def get_current_metadata(self):
		self._make_cache()
		try:
			songid = self.c.status()["songid"]
		except:
			return {"id":0, "album":"None", "artist":"None", "title":"None"}
		else:
			for i in self.metadat:
				if i["id"] == songid:
					return i

	old = {"id":-1}
	def _check(self):
		self.new = self.get_current_metadata()
		try:
			if self.new["id"] != self.old["id"]:
				self.old = self.new
				return True
			else:
				return False
		except TypeError:
			return
		except:
			raise

	def start(self):
		self._connect()

	def _now_playing(self):
		song = self.old
		print("\n::: Now playing :::\n'%s' by '%s'\nAlbum:\t'%s'\nID:\t%s\n" %(song["title"], song["artist"], song["album"], song["id"]))

class StereoProbe(UserProbe, LCDControl):
	addr = IP_ADR
	port = PORT
	okay = False
	def __init__(self):
		self.t0 = [0], [-1]
		self.open_serial()

	def _now_playing(self):
		song = self.old
		print("\n::: Now playing :::\n'%s' by '%s'\nAlbum:\t'%s'\nID:\t%s\n" %(song["title"], song["artist"], song["album"], song["id"]))
		msg = "++ '" + str(song["title"]) + "' by '" + str(song["artist"]) + "'"
		self._write(msg)

	def _time(self):
		now = dt.datetime.now().strftime("%H:%M").split(":")
		if (now[0] > self.t0[0]) or (now[1] > self.t0[1]):
			self.t0 = now
			return True
		else:
			return False

	def _update_time(self):
		t = ":".join(self.t0)
		t = "$"+t
		self._write(t)
		sleep(2)
		song = self.old
		if song["id"] != -1:
			msg = "++ '" + str(song["title"]) + "' by '" + str(song["artist"]) + "'"
			self._write(msg)
