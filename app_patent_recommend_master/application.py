from flask import Flask
import os
import sys
from flask_sqlalchemy import SQLAlchemy
import settings


TEST_LOG = __name__ + '.py'
this_function_name = sys._getframe().f_code.co_name

DEBUG = False
SECRET_KEY = os.urandom(24)

app = Flask(__name__, static_url_path="", static_folder="static")
# app.config.from_object(__name__)
# app.config.from_envvar('FLASK_SETTINGS')
app.config.from_object(settings)

db = SQLAlchemy(app)


from views import *

