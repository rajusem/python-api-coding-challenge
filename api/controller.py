import re

from flask import request, jsonify

from api import app

fun_name_pattern = '^[a-zA-Z_](.*?)[a-zA-Z0-9_]$'
digit_pattern = '\d+'
str_to_compare = 'github.com/openshift/machine-config-operator/pkg/apis/machineconfiguration.openshift.io/v1/register.go'


@app.route('/test', methods=['POST'])
def index():
    file = request.files['log-data']
    results = []

    for line in str(file.read()).split('\\n'):
        if str_to_compare in line:
            splited_values = line.split(str_to_compare)
            if len(splited_values) == 2:
                result = {"operation": 'ENTRY' if 'ENTER' in splited_values[0] else 'EXIT'}

                # get filename
                sv = splited_values[0].split(':')
                filename = sv[1].strip() + str_to_compare
                result["filename"] = filename

                # get line no
                line_no = re.findall(digit_pattern, splited_values[1])[0]
                result["line_number"] = int(line_no)

                # get function name
                temp = splited_values[1].replace(line_no, '', 1).replace(':', '', 1).strip()
                fun_name_result = re.search(fun_name_pattern, temp)
                fun_name = fun_name_result.group(0) if fun_name_result else 'anonymous'
                result["name"] = fun_name

                # if entry with same name, line_number and filename exist then no need to add entry in result
                if len(results) == 0 or len([x for x in results if
                                             x["name"] == result["name"] and x["line_number"] == result[
                                                 "line_number"] and x["filename"] == result["filename"]]) == 0:
                    results.append(result)

    # sorting based on operation so Entry results show first
    results.sort(key=lambda x: x["operation"])

    return jsonify({'result': results})
