"""This a file with taylor made responses specifically for this application"""
from flask import jsonify, make_response


class BaseClass(object):

    def __init__(self):
        """Defining the responses"""
        self.ok_status = 200
        self.created_status = 201
        self.bad_request_status = 400
        self.unauthorized_status = 401
        self.forbidden_status = 403
        self.not_found_status = 404
        self.not_acceptable_status = 406
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


