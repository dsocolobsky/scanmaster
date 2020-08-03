from flask import Flask
from pony.flask import Pony
from flask_moment import Moment

app = Flask(__name__)
Pony(app)

moment = Moment(app)

from web import database
from web import routes
