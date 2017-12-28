"""This module defines the application endpoints"""

import uuid
from functools import wraps
from flask import request, jsonify, url_for, session, render_template, redirect, flash
#from app import user_object, event_object, rsvp_object
from . import main

def login_required(f):
	"""Check if the user is in session, else redirect to login page"""
	@wraps(f)
	def login_check(*args, **kwargs):
		"""A decorated login check function"""
		if "username" in session:
			return f(*args, **kwargs)
		flash("you need to login to access this page", "warning")
		return redirect(url_for('main.login'))
	return login_check


@main.route('/')
def index():
	"""A route to render the home page"""
	return render_template("index.html")

#registration and login routes
@main.route('/auth/register', methods=['GET', 'POST'])
def register():
	"""A route to handle user"""
	if request.method == 'POST':
		username = request.form['username']
		email = request.form['email']
		password = request.form['password']
		cnfpass = request.form['cnfpass']
		#pass the details to the register method
		res = user_object.register(username, email, password, cnfpass)
		if res == "Username or email already exists."\
			or res == "Username or email can only contain alphanumeric characters"\
			or res == "passwords do not match"\
			or res == "Password too short":
			flash(res, 'warning')
			return redirect(url_for('main.register'))
		flash("Registration successfull, now login", "success")
		return redirect(url_for('main.login'))
	return render_template("signup.html")

@main.route('/auth/login', methods=['GET', 'POST'])
def login():
	"""A route to render the login page and login a user"""
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		res = user_object.login(username, password)
		if res == "successful":
			for user in user_object.user_list:
				if user['username'] == username:
					session['userid'] = user['id']
					session['username'] = username
			flash('login success', 'success')
			return redirect(url_for('main.events'))
		flash("wrong password or username", 'warning')
		return redirect(url_for('main.login'))
	return render_template("login.html")

@main.route('/logout')
def logout():
	"""A route to logout amd remove a user from the session"""
	session.pop('userid')
	session.pop('username')
	flash('you logged out', 'success')
	return redirect(url_for('main.index'))

#routes for events
@main.route('/newevent')
@login_required
def newevent():
	"""A route to render a page for creating events"""
	return render_template('events/new.html', page="create")

@main.route('/events', methods=['GET', 'POST'])
@login_required
def events():
	"""A route to return all the events available and create new events"""
	if request.method == 'POST':
		name = request.form['eventname']
		description = request.form['description']
		category = request.form['category']
		location = request.form['location']
		event_date = request.form['event_date']
		createdby = session['username']
		res = event_object.create(name, description, category, location, event_date, createdby)
		if res == "event created":
			flash("event created successfuly", "success")
			return redirect(url_for('main.myevents', page="myevents"))
		flash(res, "warning")
		return redirect(url_for('main.newevent'))
	events = event_object.view_all()
	return render_template('events/eventlist.html', events=events,\
			 page="events")

@main.route('/events/<eventid>/edit', methods=['GET','POST'])
@login_required
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
		res = event_object.update(eventid, name, description, category, location, event_date, createdby)
		if res == "Event cannot be updated, a similar event exists" \
			or res == "event can only have a future date"\
			or res == "name too short or invalid":
			flash(res, 'warning')
			return redirect(url_for('main.update_event', eventid=eventid))
		flash('event updated', 'success')
		return redirect(url_for('main.myevents'))
	res = event_object.find_by_id(eventid)
	if not res:
		flash("event not found, it might have been deleted", 'warning')
		return redirect(url_for('main.myevents'))
	return render_template('events/edit.html', event=res,\
			 page="edit")

@main.route('/events/myevents')
@login_required
def myevents():
	"""This route returns events belonging to a specific user"""
	username = session['username']
	events = event_object.createdby_filter(username)
	return render_template('events/personalEvents.html', events=events,\
			page="myevents")
	
@main.route('/events/<eventid>/delete', methods=['POST'])
@login_required
def delete_event(eventid):
	"""A route to handle deletion of events"""
	eventid = uuid.UUID(eventid)
	res = event_object.delete(eventid)
	if res == "deleted":
		flash('event deleted', 'success')
		return redirect(url_for('main.myevents'))
	flash('error, could not delete event')
	return redirect('main.myevents')
	
@main.route('/event/<eventid>/rsvp', methods=['GET', 'POST'])
@login_required
def rsvp(eventid):
	"""A route for registering a user to an event"""
	eventid = uuid.UUID(eventid)
	if request.method == 'POST':
		userid = session['userid']
		if not event_object.find_by_id(eventid):
			flash("can not rsvp to a non existing event", "warning")
			return redirect(url_for('events'))
		else:
			res = rsvp_object.create(eventid, userid)
			if res == "rsvp success":
				flash('Successfuly reserved a seat, see you then', 'success')
				return redirect(url_for('main.events'))
			flash('You already registered for this event', 'warning')
			return redirect(url_for('main.events'))
	userids = rsvp_object.view_rsvp(eventid)
	users = [user for user in user_object.user_list if user['id'] in userids]
	return render_template('events/viewrsvps.html', users=users)

@main.route('/auth/resetpass', methods=['GET','POST'])
def resetpass():
	"""Route to reset user password"""
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		cnfpass = request.form['cnfpass']
		if password != cnfpass:
			flash("passwords do not match", "warning")
			return redirect(url_for('main.resetpass'))
		res = user_object.reset_pass(username, password)
		if res == "success":
			flash('password reset, now login', "success")
			return redirect(url_for('login'))
		flash('incorect username', 'danger')
		return redirect(url_for('resetpass'))
	return render_template('resetpass.html')

@main.route('/searchevents', methods=['POST'])
def search_events():
	"""A route to search events depending on the events category or location"""
	parameter = request.form['search']
	if not parameter.strip():
		flash('please type event name or location', 'warning')
		return redirect(url_for('events', page="events"))
	else:
		events = event_object.category_filter(parameter)
		if not events:
			events = event_object.location_filter(parameter)
			if events:
				return render_template('events/eventlist.html', events=events,\
			 page="searchresults")
			flash('no events matched your search, check the input and search again', 'warning')
			return redirect(url_for('events'))
		return render_template('events/eventlist.html', events=events,\
			 page="searchresults")
