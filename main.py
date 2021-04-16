from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os

from util import parse_request_body, DatasetError
from predictor import Predictor

# Loads the environment variables from .env file for development
env_file = '.env'
if os.environ.get('FLASK_ENV') == 'production':
    env_file = '.env.production'

load_dotenv(dotenv_path=env_file)

app = Flask(__name__)


@app.route('/')
def index():
    return 'See <a href="https://github.com/JIA-0302/Analytics/blob/master/README.md">documentation</a> for usage'


@app.route('/predict-tips', methods=["POST"])
def predict_tips():
    # Validate the access token
    authorization = request.headers.get('Authorization', None)
    if authorization is None or authorization.split(' ')[1] != os.environ.get('ACCESS_TOKEN'):
        return {'error': 'Please provide a valid access token'}, 400

    # Retrieve the request body
    req_body = request.get_json()
    if req_body is None:
        return {'error': 'Please provide necessary parameters'}, 400

    try:
        # Parse the request body to retreive required parameters
        user_id, search_dates = parse_request_body(req_body)
    except Exception as err:
        print(err)
        return {'error': str(err)}, 400

    try:
        # Get predicted tips for each specified day
        predictor = Predictor(user_id=user_id, search_dates=search_dates)
        return predictor.get_predicted_tips(), 200
    except DatasetError as err:
        return {'error': str(err)}, 500
    except Exception as err:
        print(err)
        return {'error': 'Failed to predict tips for the user. Please try again later'}, 500


if __name__ == '__main__':
    app.run(debug=True)
