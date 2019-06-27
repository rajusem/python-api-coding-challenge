from flask import request, jsonify, Blueprint

# Initialize blueprint
from api.parser import Parser

parser = Blueprint('parser', __name__)


@parser.route('/log-parser', methods=['POST'])
def index():
    """
        API that parses logs generated from CI
        Call this api to parse given CI logs and it returns filtered data in Json format.
        ---
        tags:
          - python-api-codding-challenge
        consumes:
          - multipart/form-data
        parameters:
          - in: formData
            name: log-data
            type: file
            required: true
            description: File that contains log data
        responses:
          500:
            description: Error
          200:
            description: Success
          400:
           description: Bad Request
        """

    file = request.files['log-data']

    parser_obj = Parser(file)
    results = parser_obj.parse_data()

    return jsonify({'result': results})
