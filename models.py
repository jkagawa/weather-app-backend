from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import uuid
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask_login import LoginManager
from flask_marshmallow import Marshmallow
import secrets

# set variables for class instantiation
login_manager = LoginManager()
ma = Marshmallow()
db = SQLAlchemy()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model):
    id = db.Column(db.String, primary_key=True)
    first_name = db.Column(db.String(150), nullable=False, default='')
    email = db.Column(db.String(150), nullable=False, default='')
    password = db.Column(db.String, nullable=False, default='')
    g_auth_verify = db.Column(db.Boolean, nullable=False, default=False)
    token = db.Column(db.String, nullable=False, default='', unique=True)
    date_created = db.Column(db.DateTime, nullable=False, default = datetime.utcnow)

    def __init__(self, first_name='', email='', password='', g_auth_verify=False):
        self.id = self.set_id()
        self.first_name = first_name
        self.email = email
        self.password = self.set_password(password)
        self.g_auth_verify = g_auth_verify
        self.token = self.set_token(24)

    def set_token(self, length):
        return secrets.token_hex(length)

    def set_id(self):
        return str(uuid.uuid4())
    
    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash

    def __repr__(self):
        return f'User {self.email} has been added to the database'
    
class Location(db.Model):
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String(100), nullable=False, default='')
    latitude = db.Column(db.String(100), nullable=False, default='')
    longitude = db.Column(db.String(100), nullable=False, default='')
    timezone = db.Column(db.String(100), nullable=False, default='')
    location_api_id = db.Column(db.String(100), nullable=False, default='')
    date_created = db.Column(db.DateTime, nullable=False, default = datetime.utcnow)

    def __init__(self, name='', latitude='', longitude='', timezone='', location_api_id=''):
        self.id = self.set_id()
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.timezone = timezone
        self.location_api_id = location_api_id

    def __repr__(self):
        return f'The location has been added to the database: {self.name} - latitude: {self.latitude}, longitude: {self.longitude} ({self.location_api_id})'

    def set_id(self):
        return (secrets.token_urlsafe())

class SavedLocation(db.Model):
    id = db.Column(db.String, primary_key=True)
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable=False, default='')
    location_id = db.Column(db.String, db.ForeignKey('location.id'), nullable=False, default='')
    date_saved = db.Column(db.DateTime, nullable=False, default = datetime.utcnow)

    def __init__(self, user_token='', location_id=''):
        self.id = self.set_id()
        self.user_token = user_token
        self.location_id = location_id

    def __repr__(self):
        return f'The user has saved the location to their account - ID: {self.location_id}'

    def set_id(self):
        return (secrets.token_urlsafe())

class LocationSchema(ma.Schema):
    class Meta:
        fields = ['id', 'name', 'latitude', 'longitude', 'timezone', 'location_api_id']

class UserSchema(ma.Schema):
    class Meta:
        fields = ['email', 'first_name']

class AuthUserSchema(ma.Schema):
    class Meta:
        fields = ['email', 'first_name', 'token']

location_schema = LocationSchema()
location_multi_schema = LocationSchema(many=True)
user_schema = UserSchema()
loggedin_user_schema = AuthUserSchema()