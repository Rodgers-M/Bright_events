
from app import app, user_object , event_object, rsvp_object
from flask import request, json , jsonify, url_for, session, render_template, redirect, flash
import uuid

@app.route('/')
def index():
	"""A route to render the home page"""
	return render_template("index.html")

#registration and login routes
@app.route('/auth/register', methods=['GET','POST'])
def register():
	"""A route to handle user"""
	if request.method == 'POST':
		print('request')
		username = request.form['username']
		print(username)
		email = request.form['email']
		print(email)
		password = request.form['password']
		print(password)
		cnfpass = request.form['cnfpass']
		print(cnfpass)
		#pass the details to the register method
		res = user_object.register(username, email, password, cnfpass)
		if res == "Username already exists."\
			or res == "Username can only contain alphanumeric characters"\
			or res == "passwords do not match"\
			or res == "Password too short":
			flash(res, 'warning')
			return redirect(url_for('register'))
		flash("Registration successfull, now login", "success")
		return redirect(url_for('login'))
	return render_template("signup.html")

@app.route('/auth/login', methods=['GET','POST'])
def login():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		res = user_object.login(username, password)
		if res == "successful":
			for user in user_object.user_list:
				if user['username'] == username:
					session['userid'] = user['id']
					session['username'] = username
					print(session['userid'])
					print(session['username'])
			flash('login success' , 'success')
			return redirect(url_for('newevent'))
		flash("wrong password or username", 'warning')
		return redirect(url_for('login'))
	return render_template("login.html")

#routes for events
@app.route('/newevent')
def newevent():
	return render_template('events/new.html')
@app.route('/events', methods = ['GET', 'POST'])
def events():
	if request.method == 'POST':
		name = request.form['eventname']
		description = request.form['description']
		category = request.form['category']
		location = request.form['location']
		event_date = request.form['event_date']
		createdby = session['username']
		res = event_object.create(name, description, category, location, event_date, createdby)
		if res == "event exists":
			flash("a similar event exists", "warning")
			return redirect('events')
		flash("event created successfuly", "success")
		#this route will later redirect to view events
		return redirect('events')
	events = event_object.view_all()
	return render_template('events/eventlist.html', events=events)

@app.route('/events/<eventid>', methods = ['GET','PUT'])
def update_event(eventid):
	"""A route to handle event updates"""
	if request.method == 'PUT':
		eventid = uuid.UUID(eventid)
		event_details = request.get_json()
		print(eventid)
		name = request.form['eventname']
		description = request.form['description']
		category = request.form['category']
		location = request.form['location']
		event_date = request.form['event_date']
		createdby = session['userid']
		res = event_object.update(eventid, name,description, category, location, event_date, createdby)
		return res
	return render_template('events/edit.html')

@app.route('/events/<eventid>', methods=['DELETE'])
def delete_event(eventid):
	"""A route to handle deletion of events"""
	eventid = uuid.UUID(eventid)
	res = event_object.delete(eventid)
	return res

@app.route('/event/<eventid>/rsvp', methods=['GET','POST'])
def rsvp(eventid):
	"""A route for registering a user to an event"""
	eventid = uuid.UUID(eventid)
	if request.method == 'POST':
		userid = session['userid']
		res = rsvp_object.create(eventid, userid)
		return res
	userids = rsvp_object.view_rsvp(eventid)
	users = [user for user in user_object.user_list if user['id'] in userids]
	return jsonify(users)
