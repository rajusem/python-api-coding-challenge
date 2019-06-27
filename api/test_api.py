import pytest
import json
from io import BytesIO
from api import app

client = app.test_client()


def test_parse_valid_log_data():
    """
    Unit test case verifies result of cli generated data(api/test-data/data.txt)

    Log data has 2 valid entry which should come into results
    """

    with open('api/test-data/data.txt', 'rb') as fileobj:
        file_content = fileobj.read()

    data = {
        'log-data': (BytesIO(file_content), 'test')
    }

    # call api
    response = client.post(
        '/api/log-parser',
        content_type='multipart/form-data',
        data=data
    )

    # check response status code
    assert response.status_code == 200

    # convert response data to json
    json_data = json.loads(response.data)

    # check result length should be 2
    assert len(json_data["result"]) == 2

    # in result one entry should be for "ENTRY" and properties should be as verified as below.
    entry_data = [x for x in json_data["result"] if x["operation"] == "ENTRY"][0]
    assert entry_data["filename"] == "/usr/local/src/github.com/openshift/machine-config-operator/pkg/apis" \
                                     "/machineconfiguration.openshift.io/v1/register.go"
    assert entry_data["line_number"] == 32
    assert entry_data["name"] == "addKnownTypes"  # valid function name (addKnownTypes)

    # in result one entry should be for "EXIT" and properties should be as verified as below.
    exit_data = [x for x in json_data["result"] if x["operation"] == "EXIT"][0]
    assert exit_data["filename"] == "/usr/local/src/src/github.com/openshift/machine-config-operator/pkg/apis" \
                                    "/machineconfiguration.openshift.io/v1/register.go"
    assert exit_data["line_number"] == 28
    assert exit_data["name"] == "anonymous"  # invalid function name (0)


def test_parse_invalid_log_data():
    """
    Unit test case verifies result of cli generated data(api/test-data/data.txt)

    Log data has 0 valid entry which should come into results
    """

    with open('api/test-data/data2', 'rb') as fileobj:
        file_content = fileobj.read()

    data = {
        'log-data': (BytesIO(file_content), 'test')
    }

    # call api
    response = client.post(
        '/api/log-parser',
        content_type='multipart/form-data',
        data=data
    )

    # check response status code
    assert response.status_code == 200

    # convert response data to json
    json_data = json.loads(response.data)

    # check result length should be 2
    assert len(json_data["result"]) == 0
