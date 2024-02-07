from flask import Flask

from models import db
from routes import app_routes, jwt, cors

# Flask
app = Flask(__name__)

# Routes
app_routes(app)

# CORS
cors.init_app(app)

# Config
app.config.from_object('config')

# JWT
jwt.init_app(app)

# Database
db.init_app(app)

# Create database tables
with app.app_context():
    db.create_all()


if __name__ == '__main__':
    app.run(debug=True, port=5003)
