#!/usr/bin/env python
# File    : server.py ; a Flask app to control an LED and show off authentication 
# Author  : Joe McManus josephmc@alumni.cmu.edu
# Version : 0.3  02/29/2016
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


from flask import Flask, render_template, Markup, request, redirect, session
from OpenSSL import SSL
import sys 
import mraa
import time
import sqlite3
import hashlib

def getHash(passText):
	hashPass=hashlib.sha512()
	hashPass.update(passText)
	return(hashPass.hexdigest())

app = Flask(__name__)

@app.route('/')
def index():
	return render_template('template.html', bodyText="Welcome to the Intel Galileo Gen 2 using Flask")

@app.route('/led/<int:i>')
def led(i):
	if session.get('authenticated'):
		if session['authenticated'] != 'yes':
			response=redirect('/loginForm', code=302)
			return response
	else: 
		response=redirect('/loginForm', code=302)
		return response
		
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
	bodyText=Markup("Turning LED " + ledWord + "<br> <br> <a href=/logout> logout </a> <br>")
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
	
@app.route('/loginForm')
def loginForm():
	bodyText=Markup('''<form method=POST action=/login>
	Username: <input type=text name=postUser value=\"\"></input><br>
	Password: <input type=password name=postPass value=\"\"></input><br>
	<input type=submit name=submit value=\"submit\">
	</form>
	''')
	return render_template('template.html', bodyText=bodyText) 

@app.route('/login', methods=['GET', 'POST'])
def login():
	db = sqlite3.connect('server.sql3')
	db.row_factory = sqlite3.Row
	epass=getHash(request.form['postPass'])
	query="select id, username, password from users where username=? and password=?"
	t=(request.form['postUser'], epass)
	cursor=db.cursor()
	cursor.execute(query, t)
	rows = cursor.fetchall()
	if len(rows) == 1:
		bodyText=request.form['postUser'] + " " + request.form['postPass']
		bodyText=bodyText + " Success!" 
		session['authenticated']='yes'
	else:
		bodyText = "Incorect Login."

	return render_template('template.html', bodyText=bodyText)

@app.route('/logout')
def logout():
	session['authenticated']='no' 
	response=redirect('/', code=302)                       
	return response
	
if __name__ == '__main__':
	
	context=('server.crt', 'server.key')
	app.secret_key = 'ac5e7221f7d8146678b3f977f4985cf602877d2135affa9cc0eb89f4c01e68261d54df'
	#app.run(host='0.0.0.0', port=80)
	app.run(host='10.0.1.10', debug=False, port=443, ssl_context=context)
