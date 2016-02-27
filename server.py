#!/usr/bin/env python
# File    : server.py ; a Flask app to control an LED `
# Author  : Joe McManus josephmc@alumni.cmu.edu
# Version : 0.2  02/26/2016
# Copyright (C) 2016 Joe McManus
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


from flask import Flask, render_template
import sys 
import mraa
import time

app = Flask(__name__)

@app.route('/')
def index():
	return render_template('template.html', bodyText="Welcome to the Intel Galileo Gen 2 using Flask")

@app.route('/led/<int:i>')
def led(i):
	ledPostAction=i
	if ledPostAction == 0:
		ledWord="off"
		ledAction=0
	elif ledPostAction == 1:
		ledWord="on"
		ledAction=1
	else:
		return(True)
	   
	pin = mraa.Gpio(12)
	pin.dir(mraa.DIR_OUT)
	pin.write(ledAction)
	bodyText="Turning LED " + ledWord
	return render_template('template.html', bodyText=bodyText)

@app.route('/ledStatus')
def ledStatus():
	pin = mraa.Gpio(12)
	if pin.read() == 0:
		status="off"
	else: 
		status="on"
	bodyText="The LED is currently " + status
	return render_template('template.html', bodyText=bodyText) 

@app.route('/tmp')
def tmp():
	try: 
		#Initialize the MRAA pin
		pin = mraa.Aio(1) 
		#Set it to a 12 bit value
		pin.setBit(12)
	except Exception,e:
		print("Error: {:s}". format(e))
		sys.exit()
	
	rawReading = pin.read()
			
	#Galileo voltage should be the raw reading divided by 819.0
	#The reading is from 0-4095 to cover 0-5 volts
	#Or 4095/5=819.0
	galVoltage=float(rawReading / 819.0)
	tempC= (galVoltage * 100 ) - 50 
	tempF= (tempC * 9.0 / 5.0) + 32.0
	bodyText="Current Temperature: " + str(round(tempF,2)) 
	return render_template('template.html', bodyText=bodyText) 
	

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=80)
