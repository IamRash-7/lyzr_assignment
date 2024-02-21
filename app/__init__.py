from flask import Flask

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

from app.routes import api_blueprint
app.register_blueprint(api_blueprint)