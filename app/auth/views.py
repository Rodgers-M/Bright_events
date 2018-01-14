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

@auth.route('/register', methods=['POST'])
def register():
	""" a route to register a user"""
	data = request.get_json()
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
		except Exception as e:
			#an error occured when trying to register the user
			response = {'message' : str(e)}
			return jsonify(response), 401
	else:
		# there is an existing user with given email
		response = {'message' : 'a user with given email exists, please login'}
		return jsonify(response), 202

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
