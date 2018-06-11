from Stereo.Stereo3 import StereoQuery
PAGES_PATH = "/".join(__file__.split("/")[:-1])+"/pages/"

class QueryHost:
	def __init__(self, form, client):
		print("Query")
		print(list(form))
		try:
			form["search"]
		except:
			with open(PAGES_PATH + "Ceridwen.html") as f:
				self.html = f.read()
		else:
			self.client = StereoQuery(client)
			self._search(form)
			self._make_page()

	def _search(self, form):
		query = {}
		for index in ["artist", "album", "song"]:
			try:
				query[index] = str(form[index]).capitalize()
			except:
				pass
		self.query = self.client.find(**query)

	def _make_page(self):
		query = self.query
		query = sorted(query, key = lambda item: item["album"])
		print(query)
		file = PAGES_PATH + "Gwion.html"
		with open(file, 'r') as f:
			pre = f.read()
		post = """</div></body></html>"""
		if len(query) == 0:
			self.html = pre + """<h3>No Results Found</h3>""" + post
		else:
			s = "<form action='/add_songs' method='post'><button class='button' type='submit'>Add Selected</button><hr>"
			s += "<table>"
			for q in query:
				s += "<tr>"
				s += "<td width=26%>" + q['artist'] + "</td>"
				s += "<td width=26%>" + q['album'] + "</td>"
				s += "<td width=36%>" + q['title'] + "</td>"
				s += "<td width=12%><input type='checkbox' name='add' value='" + str(q["file"]) + "'>"
				s += "</tr>"
			s += "</table><form>"
			self.html = pre + s + post

	def __str__(self):
		return self.html

if __name__ == '__main__':
	q = QueryHost({"home" : None})
	print(str(q))