from blanca import app
import blanca.db

app.config.from_object(__name__) # load config from this file , flaskr.py

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE_URL='sqlite:///db.sql',
    SECRET_KEY='development key',
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)
blanca.db.init(app.config['DATABASE_URL'])

@app.route("/")
def hello():
    return "Hello, world"
