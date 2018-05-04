"""This a file with taylor made responses specifically for this application"""
from flask import jsonify, make_response


class BaseClass(object):

    def __init__(self):
        """Defining the responses"""
        self.ok_status = 200
        self.created_status = 201
        self.forbidden_status = 403
        self.not_found_status = 404
        self.not_acceptable_status = 406
        self.bad_request_status = 400
        self.unauthorized_status = 401
        self.conflict_status = 409
        self.internal_server_error_status = 500


class Success(BaseClass):
    """ The responses to successful requests """
    def complete_request(self, message):
        """ Any successful Request """
        response = jsonify({"message": message})
        return make_response(response), self.ok_status

    def create_resource(self, resource):
        """ Creation of any Resource """
        return make_response(resource), self.created_status


class Error(BaseClass):
    """The responses to requests resulting in errors"""

    def not_found(self, message):
        """When a resource is not found"""
        response = jsonify({"error": message})
        return make_response(response), self.not_found_status

    def not_acceptable(self, message):
        """ When the request is not acceptable """
        response = jsonify({"error": message})
        return make_response(response), self.not_acceptable_status

    def causes_conflict(self, message):
        """ When the request causes a conflict in the server e.g duplicate """
        response = jsonify({"error": message})
        return make_response(response), self.conflict_status

    def unauthorized(self, message):
        """ When the equest has an invalid token """
        response = jsonify({"error": message})
        return make_response(response), self.unauthorized_status

    def forbidden_action(self, message):
        """ When the request made requires a token, none provided """
        response = jsonify({"error": message})
        return make_response(response), self.forbidden_status

    def bad_request(self, message):
        """ When the request made is in the wrong format """
        response = jsonify({"error": message})
        return make_response(response), self.bad_request_status

    def internal_server_error(self, message):
        """ When there is an error in the server and has nothing to do with the user """
        response = jsonify({"error": message})
        return make_response(response), self.internal_server_error_status
