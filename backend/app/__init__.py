from flask import Flask
from dotenv import load_dotenv
import datetime
import os


load_dotenv()

app = Flask(__name__)
#app.permanent_session_lifetime = datetime.timedelta(days=50)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'.txt'}


from . import views

