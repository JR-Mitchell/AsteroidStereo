from hashlib import sha1
from flask import url_for, redirect, current_app
from os import listdir
from os.path import isfile, join
PAGES_PATH = "/".join(__file__.split("/")[:-1])+"/pages/"
USERS_PATH = "/".join(PAGES_PATH.split("/")[:-2])+"/users/"

class LoginPage:
	def __init__(self):
		with open(PAGES_PATH+"Login.html", 'r') as f:
			self.html = f.read()

	def check(self, cooki_id):
		users = [f for f in listdir(USERS_PATH) if isfile(join(USERS_PATH, f))]
		if cooki_id in users:
			return True
		else:
			return False

	def _set_cookie(self, h_uname):
		resp = current_app.make_response(redirect('/stereo'))
		resp.set_cookie("pass", value=h_uname)
		return resp

	@staticmethod
	def _get_file(uname):
		file = USERS_PATH + str(uname) + '.txt'
		try:
			f = open(file, 'r')
		except:
			return None
		else:
			udata = f.read()
			f.close()
			return udata

	def _get_pass(self, uname):
		udata = self._get_file(uname)
		if udata == None:
			return None
		else:
			print(udata)
			return udata.split("\n")[0]

	def login(self, req):
		form = req.form
		uname = sha1(str(form['uname'])).hexdigest()
		psw = sha1(str(form['psw'])).hexdigest()

		if psw == self._get_pass(uname):
			return self._set_cookie(uname)
		else:
			return redirect(url_for('root'))

	def __str__(self):
		return self.html

class RegisterPage:
	def __init__(self):
		with open(PAGES_PATH + "Register.html", 'r') as f:
			self.html = f.read()

	def _create_user(self, uname, psw):
		file = USERS_PATH + str(uname) + '.txt'
		with open(file, "w") as f:
			f.write(psw)

	def register(self, form):
		uname = str(form["uname"])
		psw = str(form["psw"])
		pswr = str(form["psw-repeat"])
		print(uname, psw)
		hname = sha1(uname).hexdigest()
		if LoginPage._get_file(hname) == None and psw == pswr and psw != '':
			hpsw = sha1(psw).hexdigest()
			self._create_user(hname, hpsw)
			return redirect(url_for('root'))
		else:
			return str(self)

	def __str__(self):
		return self.html