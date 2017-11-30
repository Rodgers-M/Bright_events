
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
		username = request.form['username']
		email = request.form['email']
		password = request.form['password']
		cnfpass = request.form['cnfpass']
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
			flash('login success' , 'success')
			return redirect(url_for('newevent'))
		flash("wrong password or username", 'warning')
		return redirect(url_for('login'))
	return render_template("login.html")

@app.route('/logout')
def logout():
	session.pop('userid')
	session.pop('username')
	flash('you logged out', 'success')
	return redirect(url_for('index'))

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

@app.route('/events/<eventid>/edit', methods = ['GET','POST'])
def update_event(eventid):
	"""A route to handle event updates"""
	eventid = uuid.UUID(eventid)
	if request.method == 'POST':
		name = request.form['eventname']
		description = request.form['description']
		category = request.form['category']
		location = request.form['location']
		event_date = request.form['event_date']
		createdby = session['username']
		res = event_object.update(eventid, name,description, category, location, event_date, createdby)
		if res == "Event cannot be updated, a similar event exists" \
			or res == "name too short or invalid":
			flash('event can not be udated, please correct the values', 'warning')
			return redirect(url_for('update_event', eventid = eventid))
		flash('event updated', 'success')
		return redirect(url_for('myevents'))
	res = event_object.find_by_id(eventid)
	if res == "event not found":
		flash("event not found, it might have been deleted", 'warning')
		return redirect(url_for('myevents'))
	return render_template('events/edit.html', event = res)

@app.route('/events/myevents')
def myevents():
	"""This route returns events belonging to a specific user"""
	username = session['username']
	events = event_object.createdby_filter(username)
	return render_template('events/personalEvents.html', events = events)
	
@app.route('/events/<eventid>/delete', methods=['POST'])
def delete_event(eventid):
	"""A route to handle deletion of events"""
	eventid = uuid.UUID(eventid)
	res = event_object.delete(eventid)
	if res == "deleted":
		flash('event deleted', 'success')
		return redirect(url_for('myevents'))
	flash('error, could not delete event')
	return redirect('myevents')
	
@app.route('/event/<eventid>/rsvp', methods=['GET','POST'])
def rsvp(eventid):
	"""A route for registering a user to an event"""
	eventid = uuid.UUID(eventid)
	if request.method == 'POST':
		userid = session['userid']
		res = rsvp_object.create(eventid, userid)
		if res == "rsvp success":
			flash('Successfuly reserved a seat, see you then', 'success')
			return redirect(url_for('events'))
		flash('You already registered for this event', 'warning')
		return redirect(url_for('events'))
	userids = rsvp_object.view_rsvp(eventid)
	users = [user for user in user_object.user_list if user['id'] in userids]
	return render_template('events/viewrsvps.html', users=users)