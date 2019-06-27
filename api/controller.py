import re

from flask import request, jsonify, Blueprint


FUN_NAME_PATTERN = '^[a-zA-Z_](.*?)[a-zA-Z0-9_]$'
DIGIT_PATTERN = '\d+'
STR_TO_COMPARE = 'github.com/openshift/machine-config-operator/pkg/apis/machineconfiguration.openshift.io/v1/register.go'


# Initialize blueprint
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
    results = []

    for line in str(file.read()).split('\\n'):
        if STR_TO_COMPARE in line:
            splited_values = line.split(STR_TO_COMPARE)
            if len(splited_values) == 2:
                result = {"operation": 'ENTRY' if 'ENTER' in splited_values[0] else 'EXIT'}

                # get filename
                sv = splited_values[0].split(':')
                filename = sv[1].strip() + STR_TO_COMPARE
                result["filename"] = filename

                # get line no
                line_no = re.findall(DIGIT_PATTERN, splited_values[1])[0]
                result["line_number"] = int(line_no)

                # get function name
                temp = splited_values[1].replace(line_no, '', 1).replace(':', '', 1).strip()
                fun_name_result = re.search(FUN_NAME_PATTERN, temp)
                fun_name = fun_name_result.group(0) if fun_name_result else 'anonymous'
                result["name"] = fun_name

                # if object available with same properties(name, line_number and filename) then no need to add entry
                # in results
                if len(results) == 0 or len([x for x in results if
                                             x["name"] == result["name"] and x["line_number"] == result[
                                                 "line_number"] and x["filename"] == result["filename"]]) == 0:
                    results.append(result)

    # sorting based on operation so Entry results show first
    results.sort(key=lambda x: x["operation"])

    return jsonify({'result': results})
