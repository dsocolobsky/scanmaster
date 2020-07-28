from flask import Flask

app = Flask(__name__)

from web import database
from web import routes