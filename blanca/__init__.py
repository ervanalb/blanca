from flask import Flask
from blanca import db

app = Flask(__name__)

import blanca.web
