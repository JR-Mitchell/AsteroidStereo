"""
http://flask.pocoo.org/docs/1.0/quickstart/#a-minimal-application
"""

from flask import Flask, redirect, request, url_for
from Server.Root import *
from Server.Login import LoginPage, RegisterPage
from Server.PlaybackHandler import *
from Server.Query import QueryHost
from Server.Juggler import PlaylistSurgeon
from Stereo.Stereo3 import StereoClient, UserProbe
app = Flask(__name__)

client = StereoClient()
client.start()
probe = UserProbe()
probe.start()
surgeon = PlaylistSurgeon(client)

def auth_for(goal):
	print("Authorising for {}".format(request.access_route))
	try:
		uniq = request.cookies.get("pass")
		if not LoginPage().check(uniq): raise KeyError
	except:
		return str(LoginPage())
	else:
		if LoginPage().check(uniq):
			return goal
		else:
			return str(LoginPage)

import sys
tmp = "/".join(PAGES_PATH.split("/")[:-2])+"/log.txt"
sys.stdout = open(tmp, 'w')
print("DEBUG :: ", PAGES_PATH)
@app.route('/', methods=['POST', 'GET'])
def root():
	print("Connection {}".format(list(request.access_route)))
	try:
		request.form["uname"]
	except:
		return auth_for(redirect(url_for("stereo")))
	else:
		return LoginPage().login(request)

@app.route('/stereo', methods=['POST', 'GET'])
def stereo():
	return auth_for(str(HomePage(probe, client)))

@app.route('/playback', methods=['POST'])
def playback():
	a = PHandler(client, request.form)
	return redirect(a._redirect())

@app.route('/misc', methods=['GET', 'POST'])
def misc():
	return auth_for(str(Pwyll()))

@app.route('/search', methods=['GET', 'POST'])
def search():
	return auth_for(str(QueryHost(request.form, client)))

@app.route('/add_songs', methods=['POST'])
def add_songs():
	try:
		val = request.form["playcache"]
	except:
		surgeon.hold(request.form.getlist('add'))
	else:
		if int(val) == 1:
			surgeon()
	finally:
		return redirect(url_for("stereo"))

@app.route('/register', methods=['POST', 'GET'])
def register():
	try:
		request.form["psw-repeat"]
	except:
		return str(RegisterPage())
	else:
		return RegisterPage().register(request.form)

app.run("0.0.0.0", 5666)