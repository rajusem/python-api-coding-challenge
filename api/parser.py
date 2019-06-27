import re

FUN_NAME_PATTERN = '^[a-zA-Z_](.*?)[a-zA-Z0-9_]$'
DIGIT_PATTERN = '\d+'
STR_TO_COMPARE = 'github.com/openshift/machine-config-operator/pkg/apis/machineconfiguration.openshift.io/v1/register.go'


class Parser:
    """
    A class that contains parser logic for CI logs.
    ...
    Attributes
    ----------
    file : file
        file that contains logs generated from CI

    Methods
    -------
    parse_data()
        Parse CI logs and it returns filtered data
    """

    def __init__(self, file):
        """
        :param file: file that contains logs generated from CI
        """
        self.file = file

    def parse_data(self):
        """
        Method contains parse logic of CI logs
        ---
        :return: filtered data
        """
        results = []
        for line in str(self.file.read()).split('\\n'):
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
                    result["name"] = self.__get_fun_name(splited_values[1].replace(line_no, '', 1).replace(':', '', 1).strip())

                    # if object available with same properties(name, line_number and filename) then no need to add entry
                    # in results
                    if len(results) == 0 or len([x for x in results if
                                                 x["name"] == result["name"] and x["line_number"] == result[
                                                     "line_number"] and x["filename"] == result["filename"]]) == 0:
                        results.append(result)

        # sorting based on operation so Entry results show first
        results.sort(key=lambda x: x["operation"])

        return results

    def __get_fun_name(self, str):
        """
        Method to get function name from given string
        ---
        :param str: string that contains function name
        :return: function name
        """
        fun_name_result = re.search(FUN_NAME_PATTERN, str)
        return fun_name_result.group(0) if fun_name_result else 'anonymous'
