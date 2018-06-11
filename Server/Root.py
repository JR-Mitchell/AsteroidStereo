PAGES_PATH = "/".join(__file__.split("/")[:-1])+"/pages/"

class HomePage:
	def __init__(self, probe, client):
		file = PAGES_PATH+"Home.html"
		with open(file, 'r') as f:
			self.html = f.read()
		met = probe.get_current_metadata()
		vol = probe.c.status()["volume"]
		self.html = self.html.replace("??!!", met["title"])
		self.html = self.html.replace("!!??", met["artist"])
		self.html = self.html.replace("!!!?", vol)
		self.html = self.html.replace("??xx!!", str(client.current_playlist))

	def __str__(self):
		return self.html

class Pwyll():
	def __init__(self):
		file = PAGES_PATH+"Pwyll.html"
		with open(file, 'r') as f:
			self.html = f.read()
	def __str__(self):
		return self.html

if __name__ == "__main__":
	print(str(HomePage()))
