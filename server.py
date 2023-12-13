from flask import Flask, request, jsonify
import pretty_errors
import pprint
import logging
from a2wsgi import WSGIMiddleware
from main import main

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
def index():
    """
    echo endpoint for server health check 
    """
    return jsonify({"status": "success", "message": "Hello World!"}), 200


@app.route('/lead_auto_assignment', methods=['POST'])
def lead_auto_assignment():
    """
    lead auto assignment endpoint
    """
    try:
        # receiving lead payload
        payload = request.get_json()
        logging.info(f"PAYLOAD RECEIVED -- {pprint.pformat(payload)}\n")

        # extracting useful information from the payload
        postalcode = payload.get("listing_zip")
        listing_province = payload.get("listing_province")
        buyer_city = payload.get("buyer_city")
        buyer_province = payload.get("buyer_province")

        # executing lead auto assignment function; returning result
        result = main(postalcode, listing_province, buyer_city, buyer_province)
        return jsonify(result), 200
    
    except Exception as e:
        error_message = {"status": "fail", "error": "Bad request", "details": str(e)}
        logging.error(f"\n!!! SERVER ERROR OCCURRED -- {str(e)}\n")
        return jsonify(error_message), 400


app = WSGIMiddleware(app)
if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')
