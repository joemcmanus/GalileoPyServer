#!/usr/bin/env python
# File    : server.py ; a Flask app to control an LED `
# Author  : Joe McManus josephmc@alumni.cmu.edu
# Version : 0.1  02/25/2016
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


from flask import Flask
import sys 
import mraa
import time

app = Flask(__name__)

def printHeader():
	return '''<html> <head>              
	 <title> Galileo Using Flask </title>
	 </head>                                   
	 <body>
	 <center>
	  <a href=/led/1> Turn LED On <a/> | <a href=/led/0> Turn LED Off </a> | 
	  <a href=/ledStatus> Check LED Status </a> |  <a href=/tmp> Display the Temperature </a> 
	  <hr> <br>'''

def printFooter(): 
	return '''</body></html>'''

@app.route('/')
def index():
	content=printHeader()
	content=content +  " Welcome to the Intel Galileo Gen 2 using Flask" 
	content=content + printFooter()
	return(content)

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
	   
	content=printHeader() + "Turning LED " + ledWord
	pin = mraa.Gpio(12)
	pin.dir(mraa.DIR_OUT)
	pin.write(ledAction)
	content=content+printFooter()
	return(content)

@app.route('/ledStatus')
def ledStatus():
	content=printHeader() + "The LED is currently "
	pin = mraa.Gpio(12)
	if pin.read() == 0:
		status="off"
	else: 
		status="on"
	content=content+ status + printFooter()
	return(content)

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
	content=printHeader() + "Current Temperature: " + str(round(tempF,2)) + "<br><a href=/tmp> Refresh Temp</a>" + printFooter()    
	return(content)
	

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=80)
