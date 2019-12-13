"""A Python Flask REST API BoilerPlate (CRUD) Style"""

import argparse
import os
from flask import Flask, jsonify, make_response, request
from flask_cors import CORS
# from routes import request_api
import kra

APP = Flask(__name__)


# APP.register_blueprint(request_api.get_blueprint())

@APP.route("/")
def isActive():
    return "Hello KRA World!"



@APP.route('/get_kra', methods=['POST'])
def get_kra_details():
    try:
        pan_number = request.json['kra']
        print(pan_number)
        kra_details = kra.scrap_kra(pan_number)
        # return jsonify(kra_details), 200
        return make_response(jsonify(kra_details), 200)

    except Exception as err:
        print(err)
        return make_response(jsonify({'error': err}), 500)
        # return jsonify({"msg":"something went wrong!"}), 500



@APP.errorhandler(400)
def handle_400_error(_error):
    """Return a http 400 error to client"""
    return make_response(jsonify({'error': 'Misunderstood'}), 400)


@APP.errorhandler(401)
def handle_401_error(_error):
    """Return a http 401 error to client"""
    return make_response(jsonify({'error': 'Unauthorised'}), 401)


@APP.errorhandler(404)
def handle_404_error(_error):
    """Return a http 404 error to client"""
    return make_response(jsonify({'error': 'Not found'}), 404)


@APP.errorhandler(500)
def handle_500_error(_error):
    """Return a http 500 error to client"""
    return make_response(jsonify({'error': 'Server error'}), 500)


if __name__ == '__main__':

    PARSER = argparse.ArgumentParser(
        description="Seans-Python-Flask-REST-Boilerplate")

    PARSER.add_argument('--debug', action='store_true',
                        help="Use flask debug/dev mode with file change reloading")
    ARGS = PARSER.parse_args()

    PORT = int(os.environ.get('PORT', 5000))

    if ARGS.debug:
        print("Running in debug mode")
        CORS = CORS(APP)
        APP.run(host='0.0.0.0', port=PORT, debug=True)
    else:
        APP.run(host='127.0.0.1', port=PORT, debug=False)
