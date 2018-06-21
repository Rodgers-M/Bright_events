import re
from datetime import date, datetime
from sqlalchemy import cast , Date
from flask import request, jsonify,g
from app.models import Events
from . import api

def validate_data(data):
    """validate the event details and return appropriate message"""
    if len(data['name'].strip()) < 3 or not re.match("^[a-zA-Z0-9_ ]*$", data['name'].strip()):
        return "event name should only contain alphanemeric characters and be at least 3 characters"
    elif len(data['location'].strip()) < 3 or not re.match("^[a-zA-Z0-9_ ]*$", data['location'].strip()):
        return "event location should only contain alphanemeric characters and be at least 3 characters"
    elif len(data['category'].strip())<3 or not re.match("^[a-zA-Z0-9_ ]*$", data['category'].strip()):
        return "event category should only contain alphanemeric characters and be at least 3 characters"
    else:
        return "valid"

def validate_date(event_date):
    """check that the event date is not past"""
    try:
        date = datetime.strptime(event_date, '%Y-%m-%d').date()
    except ValueError:
        return "incorrect date format, should be YYYY-MM-DD"
    if date < date.today():
        return "event cannot have a past date"
    return "valid"

def make_event_list(events):
    """convert the list of event objects and convert them to json"""
    event_list = []
    for event in events:
        json_event = event.to_json()
        event_list.append(json_event)
    return event_list

@api.route('/events/create', methods=['POST'])
def create():
    """a route to handle creating an event"""
    event_details = request.get_json()
    check_details = validate_data(event_details)
    check_date = validate_date(event_details['event_date'])
    #check if the data was confirmed valid
    if check_details is not "valid":
        return jsonify({"message" : check_details}), 400
    elif check_date is not "valid":
        return jsonify({"message" : check_date}), 400
    else:
        name = event_details['name']
        description = event_details['description']
        category = event_details['category']
        location = event_details['location']
        event_date = event_details['event_date']
        created_by = g.user
        #check if the user has an event with a similar name and location
        existing_event = [event for event in g.user.events if event.name == name \
            and event.location == location]
        if not existing_event:
            #create the event if does not exist
            event = Events(name=name, description=description, category=category, \
                location=location, event_date=event_date, created_by=created_by)
            event.save()
            response = event.to_json()
            return jsonify(response), 201
        return jsonify({"message": "you have a similar event in the same location"}), 302

@api.route('/events/all')
def get_all():
    """fetch all events available"""
    # fetch the first 15 events based on event date
    page = request.args.get("page", default=1, type=int)
    per_page = request.args.get("limit", default=15, type=int)
    # fetch matching events from the database
    result = Events.query.filter(cast(Events.event_date, Date) >= date.today())\
        .paginate(page, per_page, error_out=False)
    if result.items:
        event_list = make_event_list(result.items)
        print(jsonify(event_list))
        return jsonify({"message": "all events, paginated", 'event_list': event_list}), 200
    event_list = []
    return jsonify({"message" : "this page has no events, or no events available",
        'event_list': event_list}), 200

@api.route('/events/myevents')
def my_events():
    """fetch all events belonging to a particular user"""
    events = g.user.events
    if events:
        event_list = make_event_list(events)
        return jsonify({"message": "my events, paginated", 'event_list': event_list}), 200
    event_list = []
    return jsonify({"message": "you have not created any events yet",
            'event_list': event_list}), 200


@api.route('/events/<int:event_id>', methods=['PUT', 'DELETE', 'GET'])
def manipulate_event(event_id):
    """update or delete an event"""
    event = Events.get_event_by_id(event_id)
    if event:
        # make sure the events is modified by the right person
        if event.created_by.username == g.user.username:
            if request.method == 'PUT':
                event_details = request.get_json()  # get the incoming details
                # update the details accordingly
                event.name = event_details['name']
                event.description = event_details['description']
                event.category = event_details['category']
                event.location = event_details['location']
                event.event_date = event_details['event_date']
                # save the event back to the database
                event.save()
                return jsonify({
                    "message": "event updated successfully",
                    "event": event.to_json()
                    }), 200
            elif request.method == 'GET':
                # return the event with the given id
                found_event = event.to_json()
                return jsonify(found_event), 200
            else:
                # if the request method is delete
                event.delete()
                return jsonify({"message": "event deleted successfully"}), 200
        return jsonify({"message": "you can not modify the event"})
    return jsonify({"message": "no event with given id found"}), 404


@api.route('/events/<int:event_id>/rsvp', methods=['POST', 'GET', 'DELETE'])
def rsvp(event_id):
    """register a user to an event"""
    event = Events.get_event_by_id(event_id)
    if event:
        if request.method == 'POST':
            response = event.add_rsvp(g.user)
            if response == "rsvp success":
                return jsonify({"message": "rsvp success, see you then",
                    'event': event.to_json()}), 201
            return jsonify({"message": "already registered for this event"}), 302
        if request.method == 'DELETE':
            event.delete_rsvp(g.user)
            return jsonify({'message': 'rsvp cancelled', 'event': event.to_json()}), 200
        rsvps = event.rsvps.all()
        if rsvps:
            rsvp_list = []
            for user in rsvps:
                rsvp = {
                    "username": user.username,
                    "email": user.email
                }
                rsvp_list.append(rsvp)
            return jsonify(rsvp_list), 200
        return jsonify({"message": "no users have responded to this event yet"}),200
    return jsonify({"message": "event does not exist"}), 404

@api.route('/events/myrsvps')
def my_rsvps():
    """return the list of events that user has responded to"""
    rsvps = g.user.myrsvps.all()
    if rsvps:
        rsvp_list = []
        for event in rsvps:
            rsvp = {
                "event name" : event.name,
                "location" : event.location,
                "orgarniser" : event.created_by.username,
                "event date" : event.event_date
            }
            rsvp_list.append(rsvp)
        return jsonify(rsvp_list), 200
    return jsonify({"message" : "you have not responded to any events yet"}), 200

@api.route('/events/filter')
def events_filter():
    """filter events by location or category"""
    #get the incoming parameters
    location = request.args.get("location")
    category = request.args.get("category")
    #get the given page and number of events or set them to default
    page = request.args.get("page", default=1, type=int)
    per_page = request.args.get("limit", default=15, type=int)
    #check which parameter was given and use it to query the database
    if location and category:
        #if both location and category have been given,filter by both
        found_events = Events.filter_events(location, category, page, per_page)
        if found_events.items:
            event_list = make_event_list(found_events.items)
            return jsonify(event_list), 200
        return jsonify({"message" : "there are no more {} events in {}".format(category, location)}), 404
    elif location:
        found_events = Events.get_events_by_location(location, page, per_page)
        if found_events.items:
            event_list = make_event_list(found_events.items)
            return jsonify(event_list), 200
        return jsonify({"message" : "there are no more events in {}".format(location)}), 404
    elif category:
        found_events = Events.get_events_by_category(category, page, per_page)
        if found_events.items:
            event_list = make_event_list(found_events.items)
            return jsonify(event_list), 200
        return jsonify({"message" : "there are no more {} events".format(category)}), 404
    else:
        return jsonify({"message" : "can not search events with the given parameter"}), 400


@api.route('/events/search')
def search():
    """search events given an event name"""
    #get the name given
    name = request.args.get('q')
    #get the given page and number of events or set them to default
    page = request.args.get("page", default=1, type=int)
    per_page = request.args.get("limit", default=15, type=int)
    if name:
        found_events = Events.get_events_by_name(name, page, per_page)
    if found_events.items:
        event_list = make_event_list(found_events.items)
        return jsonify(event_list), 200
    return jsonify({"message" : "there are no more events matching the given name"}), 404
    return jsonify({"message" : "can not search events, provide event name"}), 400



