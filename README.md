[![Build Status](https://travis-ci.org/Rodgers-M/Bright_events.svg?branch=dev)](https://travis-ci.org/Rodgers-M/Bright_events) [![Coverage Status](https://coveralls.io/repos/github/Rodgers-M/Bright_events/badge.svg?branch=dev)](https://coveralls.io/github/Rodgers-M/Bright_events?branch=dev) [![Codacy Badge](https://api.codacy.com/project/badge/Grade/1a11748e7fa74e46aef7bdf6f09f1bf0)](https://www.codacy.com/app/Rodgers-M/Bright_events?utm_source=github.com&utm_medium=referral&utm_content=Rodgers-M/Bright_events&utm_campaign=badger) [![Maintainability](https://api.codeclimate.com/v1/badges/1c3a0ec277de71d59f8f/maintainability)](https://codeclimate.com/github/Rodgers-M/Bright_events/maintainability)


# Welcome to Bright events
A web application that provides a platform for event organizers to create and manage different types of events. 

**Application Features**

* Creating Events
* Events RSVP 


A user can perform the following :

* create an event
* view the events they have created
* edit and update the event. 
* delete the event created.
* view RSVPs to that event.

Other users can view the events posted and can respond to them (RSVP).
The users can also search events based on location or category

**Application demo**

* To interact with the application via the browser,visit the following url
    
     * [rodgerbrightevents](https://rogderbrightevents.herokuapp.com/api/v1)
    
* To interact with the API via Postman, use the link below
    
    * https://rodgerbrighteventsapi.herokuapp.com/api/v1

    then use the following endpoints to perform the specified tasks
    
    EndPoint                            | Functionality
    ------------------------            | ----------------------
    POST /auth/register                 | Create a user account
    POST /auth/login                    | Log in a user
    POST /events                        | Create an event
    GET /events                         | Retrieve existing events
    POST /event/< eventid >/rsvp        | Register a user to an event
    GET  /event/< eventid >/rsp         | Retrieve users who responded to the event
    PUT /api/events/< eventid >/edit    | Update an event
    DELETE /api/events/< eventid >      | Delete event


    
**Getting started with the app**

**Technologies used to build the application**

* [Python 3.6](https://docs.python.org/3/)

* [Flask](http://flask.pocoo.org/)

* [PostgreSQL](https://www.postgresql.org/)

* [flask sqlalchemy](http://flask-sqlalchemy.pocoo.org/2.3/)

* [JWT](auth0.com/docs/jwt)

**Running the app server**

 * Clone the repository
 * install python3(preferable python 3.6)
 * Navigate to project folder
 * Create a virtual environment
 * Activate virtual environment
 * Use `python run.py` to run the server

**Running tests**

* Install nosetests 
* navigate to project folder
* Use `nosetests tests/` to run the tests


**API endpoints**

**These endpoints can be tested using postman**

* POST /api/v1/auth/register   					create user acccount

* POST /api/v1/ auth/login						login an existing user

* GET  /api/events  								Retrieve events

* POST /api/events/								Create an event	

* POST /api/events/< eventid >/delete   			Delete an event

* POST /api/events/< eventid >/edit				Edit an event			

* POST /api/event/< eventid >/rsvp    			RSVP to an event

* GET /api/event/< eventid >/rsvp    			Retrieve event RSVPs
