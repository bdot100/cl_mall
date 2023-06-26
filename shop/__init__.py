from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_uploads import IMAGES, UploadSet, configure_uploads
import os
from werkzeug.utils import secure_filename


#basedir for our uploads
basedir = os.path.abspath(os.path.dirname(__file__))

# create the extension
db = SQLAlchemy()
# create the app
app = Flask(__name__)
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///cl_mall.db"
app.config["SECRET_KEY"] = "kskjiuesksksahsdjdk2732654skskjs6"
app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(basedir, 'static/images')

photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)

# initialize the app with the extension
db.init_app(app)
bcrypt = Bcrypt(app)

from shop.admin import routes
from shop.products import routes