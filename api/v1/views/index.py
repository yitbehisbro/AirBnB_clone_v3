#!/usr/bin/python3
""" Index file module """
from api.v1.views.__init__ import app_views
from flask import jsonify

@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """ Displays the status """
    stat = {"status": "OK"}
    return jsonify(stat)
