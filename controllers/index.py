from flask import *
from extensions import mysql
from flask import Flask, session, redirect, url_for, escape, request, flash
import hashlib
import uuid
import ast


index = Blueprint('index', __name__, template_folder='templates') #, url_prefix="/04d8ee3a8730446aa2b4/pa3")


@index.route('/', methods=['GET'])
def my_route():
	#print 'GETTING'
	return render_template("index.html", name='login')

@index.route('/', methods=['POST'])
def index_route():

	if "username" in session:
	 	return redirect(url_for('main.main_route'))    ### Have to change

	if request.method == 'POST':
		
		# Get user information
		request.form = ast.literal_eval(request.data)
		emailIn = request.form['email']
		passIn = request.form['password'] #get input
		prevURL = request.form.get("prevURL") #redirect address
	

		#Check if username exists
		cur = mysql.connection.cursor()
		cur.execute("SELECT * FROM User WHERE email = '"+emailIn+"'")
		email = cur.fetchall()
		if len(email) == 0:
			return redirect(url_for('index.index_route'))


		#Salt and hash check
		algorithm = 'sha512'
		user_pass = email[0][5] #usernames password info
		user_pass = user_pass.split('$')

		m = hashlib.new(algorithm)
		m.update(user_pass[1] + passIn)
		password_hash = m.hexdigest()

		#Check if passed in password matches actual password
		if password_hash != user_pass[2]:
			return redirect(url_for('index.index_route'))


		# Set up user session
		session['email'] = email[0][1] 
		session['skype_username'] = email[0][2]
		session['firstname'] = email[0][3]
		session['lastname'] = email[0][4]
		session['specialty'] = email[0][6]
		session['hospital_id'] = email[0][7]
		session['dr_or_emt'] = email[0][8]


		usertype = 'emt'
		if session['dr_or_emt']:
			usertype = 'dr'


	return jsonify(message="Success!", user_type=usertype, username=session['email'], user_id=email[0][0]) 
