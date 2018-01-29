import re
from flask import request, jsonify, g
from app.models import User
from . import auth

@auth.before_app_request
def before_request():
	"""get the user bafore every request"""
	if request.endpoint and request.blueprint != 'auth':
		auth_header = request.headers.get('Authorization')
		g.user = None
		if auth_header:
			access_token = auth_header.split(" ")[1]
			if access_token:
				#try decoding the token and get the user_id
				res = User.decode_token(access_token)
				if isinstance(res, int):
					#check if no error in string format was returned
					#find the user with the id on the token
					user = User.query.filter_by(id=res).first()
					g.user = user
					return
				return jsonify({"message" : res}), 401
			return jsonify({"message" : "acess token is missing"}), 401
		return jsonify({"message" : "Authorization header is missing"}), 401

def validdate_data(data):
	"""validate user details"""
	try:
		if not  re.match("^[a-zA-Z0-9_]*$", data['username'].strip())\
		or not re.match("^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", data['email'].strip()):
			return "username or email must be valid can only contain alphanumeric characters"
		elif len(data['username'].strip()) < 3:
			return "username must be more than 3 characters"
		elif data['password'] != data['cnfpassword']:
			return "passwords do not match"
		elif len(data['password'].strip()) < 6:
			return "Password too short"
		else:
			return "valid"
	except Exception as error:
		return "please provide all the fields, missing " + str(error)

@auth.route('/register', methods=['POST'])
def register():
	""" a route to register a user"""
	data = request.get_json()
	#validate the data
	res = validdate_data(data)
	if res is "valid":
		user = User.query.filter((User.email==data['email']) | (User.username==data['username'])).first()
		if not user:
			#if no user with matching email
			try:
				username = data['username']
				email = data['email']
				password = data['password']
				user = User(username=username, email=email, password=password)
				user.save()

				#registration was successful
				response = {'message' : "registration successful, now login"}
				return jsonify(response), 201
			except Exception as error:
				#an error occured when trying to register the user
				response = {'message' : str(error)}
				return jsonify(response), 401
		else:
			# there is an existing user with given email
			response = {'message' : 'email or username exists, please login or chose another username'}
			return jsonify(response), 202
	return jsonify({"message" : res}), 400

@auth.route('/login', methods=['POST'])
def login():
	"""a route to handle user login and access token generation"""
	data = request.get_json()
	try:
		user = User.query.filter_by(username=data['username']).first()

		#verify found user details
		if user and user.verify_password(data['password']):
			#user details are valid hence generate the access token
			access_token = user.generate_token()
			response = {
				'message': 'login successful.',
				'access_token':  access_token.decode()
			}
			return jsonify(response), 200
		else:
			#no user found, return an error message
			response = {'message': 'invalid username or password, Please try again'}
			return jsonify(response), 401
	except Exception as e:
		#an error occured in the server
		response = {'message': str(e)}
		return jsonify(response), 500
