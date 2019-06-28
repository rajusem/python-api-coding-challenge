# python-api-coding-challenge

This is python project, having one api that parses CI logs and give result in json format. In this code we used few frameworks listed below.
* **Flask** for rest api
* **flasgger** for OpenAPI documentation(swagger)
* **gunicorn** for WSGI HTTP Server
* **pytest** for unit testing  


### Steps to Run Project Locally 
Go to poject folder and run below commands.
```bash
pip3 install -r requirements.txt
gunicorn --workers=2 -b 0.0.0.0:5000 run:app
```

### Parse CI Logs
```bash
POST /api/log-parser
content-type: multipart/form-data
parameters:
  log-data : file which contains CI logs 
```

### Swagger UI
![swagger.png](swagger.png)


### Hosted api
Hosted api into **openshift** platform. You can test the same using Swagger UI by following below steps. 
1. Open swagger UI : http://python-api-challenge.apps.us-west-2.online-starter.openshift.com/apidocs/#/python-api-codding-challenge/post_api_log_parser
2. Click on **Try it out** button 
3. Browse CI log file from your system and select the same. (Download sample CI logs from [here](https://github.com/rajusem/python-api-coding-challenge/blob/master/api/test-data/data.txt)) 
4. Click on **Execute** button
