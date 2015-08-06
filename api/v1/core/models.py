from api.v1.models import Document, db
from flask_login import UserMixin


class User(Document, UserMixin):
	
	statuses = ['inactive', 'active', 'suspended']
	
	name = db.StringField()
	username = db.StringField()
	email = db.EmailField()
	password = db.StringField()
	status = db.StringField(choices=statuses)
	
	
class Session(Document):
	# Idea: Each time a token is used, send a new access token back to the client
	
	statuses = ['logged in', 'logged out']
	
	user = db.ReferenceField(User, required=True)
	access_token = db.StringField(required=True)
	
	
anonymous = User(email='_anon').save()