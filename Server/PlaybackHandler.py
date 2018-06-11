from flask import url_for
import os
PAGES_PATH = "/".join(__file__.split("/")[:-1])+"/pages/"

class PHandler():
	def __init__(self,  mpd_client, flask_request):
		self.client = mpd_client
		self.main=False					#redirect to main page; only used if 'play' POST request
		self.req = flask_request
		self._parse()

	def _redirect(self):
		if self.main:
			return url_for("root")
		else:
			return url_for("misc")

	def _parse(self):
		keys = self.req.keys()
		print(self.req)
		if 'play' in keys:
			self._play(int(self.req["play"]))
		if ('next' in keys) and (int(self.req["next"]) == 1):
			self.client.next()
			self.main=True
		if ('playlist' in keys) and (int(self.req['playlist']) == 1):
			a = self._playlist()
			self._make_page(a, title="Playlists")
		if 'load' in keys:
			self._load(int(self.req['load']))
			self.main=True
		if ('list' in keys) and (int(self.req['list']) == 1):
			a = self._list()
			self._make_page(a, title="Song List")
		if 'vol' in keys:
			self.main = True
			self._set_vol(int(self.req["vol"]))
		if 'song' in keys:
			self.main = True
			self.client.play(int(self.req["song"]))
		if ('toggle' in keys) and (1 == int(self.req['toggle'])):
			loc = "/".join(__file__.split("/")[:-2])
			cmd = "python "+loc+"/OnOff.py"
			os.popen(cmd)
			self.main=True

	def _set_vol(self, inc):
		vol = int(self.client.c.status()["volume"])
		if inc == 2:
			vol += 5
		if inc == 1:
			vol -= 5
		self.client.setvol(vol)

	def _list(self):
		self.client._make_cache()
		all_sg = []
		for i in self.client.metadat:
			s = """<button type="submit" name="song" value={}>play</button>""".format(i["id"])
			s += "Artist:\t<b>%s</b>\nAlbum:\t%s\nSong:\t<b>%s</b>\nID:\t%s\n" %(i["artist"], i["album"], i["title"], i["id"])
			all_sg.append(s)
		return all_sg

	def _playlist(self):
		self.client._make_cache()
		pl = self.client.plcache
		all_pl = []
		for i, name in pl.items():
			s = """<button type="submit" name="load" value="{}">Load {}</button>""".format(i, i)
			s += """Playlist: #{}\t'{}'\n""".format(i, name)
			all_pl.append(s)
		return all_pl

	def _play(self, bool):
		if bool == 1:
			self.client.play()
		elif bool == 0:
			self.client.pause()
		self.main = True

	def _load(self, num):
		self.client.load_newplaylist(num)

	def _make_page(self, _list, title="Pwyll"):
		pwyll = PAGES_PATH+"Pwyll.html"
		html = """<html><title>{}</title><body><h2>{}</h2><hr>\n<form action="playback" method="post">""".format(title, title)
		for item in _list:
			s = "<p>{}</p>\n".format(item)
			html+=s
		html+="</form></body></html>"
		with open(pwyll, 'w') as f:
			f.write(html)


