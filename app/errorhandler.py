from flask import jsonify, make_response

def not_found(error):
    """Handle 404 error"""
    return make_response(
        jsonify({
            "message": "Resource not found, Check the url and try again"
        })), 404

def bad_request(error):
    """Handle 400 error"""
    return make_response(
        jsonify({
            "message": "Please check your inputs, inputs should be in valid JSON formatt"
        })), 400

def internal_server_error(error):
    """Handle 500 error"""
    return make_response(
        jsonify({
            "message": "something went wrong while in the sever, please try again"
        })), 500
