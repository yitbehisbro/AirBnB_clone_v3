#!/usr/bin/python3
""" App module """
from models import storage
from api.v1.views import app_views
from flask import Flask
from os import getenv
from flask import make_response
from flask import jsonify

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_db(exception):
    """ Tear down method """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """ Not found handler """
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    HBNB_API_HOST = getenv('HBNB_API_HOST')
    HBNB_API_PORT = getenv('HBNB_API_PORT')

    if HBNB_API_HOST and HBNB_API_PORT:
        app.run(host=HBNB_API_HOST, port=HBNB_API_PORT, threaded=True)
    app.run(host='0.0.0.0', port=5000, threaded=True)
