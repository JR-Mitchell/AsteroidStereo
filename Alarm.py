import serial
from time import sleep
from Stereo.Stereo3 import StereoClient
import datetime as dt
from subprocess import call

class WTime:
	mon = "8:00"
	tue = "7:00"
	wed = "6:30"
	thu = "6:30"
	fri = "7:00"
	sat = "10:00"
	sun = "10:00"

class Stereo:
	def __init__(self):
		path = '/dev/ttyACM0'
		self.ser = serial.Serial(path, 9600, timeout=0.01)
		self.ser.flushInput()
		self.ser.flushOutput()
		sleep(4)

	def _play_song(self):
		sc = StereoClient()
		sc.start()
		sc.setvol(100)
		sc.c.load("nekro")
		sleep(1)
		i = int(sc.c.status()["playlistlength"])
		i -= 39
		i += 17
		sc.play(i)


	def toggle(self):
		self.ser.write(b"..toggle..\n")
		self._play_song()

class Clock:
	def __init__(self):
		now = dt.datetime.now()
		self.day = "".join(list(now.strftime("%A").lower())[:3])
		ct = now.strftime("%H:%M").split(":")
		self.time = int(ct[0])*60 + int(ct[1])

	def _get_wtime(self):
		wt = WTime.__dict__[self.day]
		wt = wt.split(":")
		return int(wt[0])*60 + int(wt[1])

	def _ring(self):
		stereo = Stereo()
		stereo.toggle()
		print("RINGING")

	def check_times(self):
		print("Wake Time ", self._get_wtime())
		print("Self Time ", self.time)
		if ( self._get_wtime() <= self.time ) and (self.time < self._get_wtime() + 10):
			self._ring()
			return 0
		else: return self._get_wtime() - self.time 

class Alarm:
	def __init__(self):
		self.on = True
		self.loopAlarm()

	def _wakeup(self):
		diff = Clock().check_times()
		if diff == 0:
			return 11
		if diff < 0:
			return 24*60 - Clock().time + 2
		if diff > 1:
			return (diff - 1)
		else: return 1/60.0

	def loopAlarm(self):
		while self.on:
			stime = self._wakeup() * 60.0
			print("Sleeping for ", stime, " seconds")
			sleep(stime)

if __name__ == "__main__":
	Alarm()





