from flask import Flask
from config import Config
from extensions import db, ma, migrate  

# Initialize the Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Bind the app to the extensions
db.init_app(app)
ma.init_app(app)
migrate.init_app(app, db)

# Import your models and routes after initializing the app
from models import *
from routes import *

if __name__ == '__main__':
    app.run(debug=True, port=5555)
