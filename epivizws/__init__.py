"""
    Initialize the package
"""

from flask import Flask, request, jsonify, Response
from flask_sqlalchemy import SQLAlchemy
from epivizws.config import app_config
from ujson import dumps

app = Flask(__name__)
app.config.from_object(app_config)
db = SQLAlchemy(app)

from epivizws.requests import create_request

def add_cors_headers(response):
    """
    Add access control allow headers to response

    Args:
     response: Flask response to be sent

    Returns:
     response: Flask response with access control allow headers set
    """
    response.headers['Access-Control-Allow-Origin'] = '*'
    if request.method == 'OPTIONS':
        response.headers['Access-Control-Allow-Methods'] = 'DELETE, GET, POST, PUT'
        headers = request.headers.get('Access-Control-Request-Headers')
        if headers:
            response.headers['Access-Control-Allow-Headers'] = headers
    return response

app.after_request(add_cors_headers)

@app.route("/", methods=["POST", "OPTIONS", "GET"])
def process_request():
    """
        routes the request to the appropriate function based on the request `action` parameter.

        Returns:
            JSON result
    """

    if request.method == "OPTIONS":
        res = jsonify({})
        res.headers['Access-Control-Allow-Origin'] = '*'
        res.headers['Access-Control-Allow-Headers'] = '*'
        return res

    param_action = request.values.get("action")
    param_id = request.values.get("requestId")
    version = request.values.get("version")

    epiviz_request = create_request(param_action, request.values)
    result, error = epiviz_request.get_data()

    return Response(response=dumps({"requestId": int(param_id),
                                    "type": "response",
                                    "error": error,
                                    "data": result
                                }),
                    status=200,
                    mimetype="application/json")
    