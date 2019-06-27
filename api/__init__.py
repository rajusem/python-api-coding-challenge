from flask import Flask
from flasgger import Swagger

# initialize flask app
app = Flask(__name__)

# enable swagger documentation
Swagger(app)

# register flask module
from api.controller import parser
app.register_blueprint(parser, url_prefix='/api')
