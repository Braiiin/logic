from logic.v1.models import Document, db


class User(Document):
	
	statuses = Document.choices('inactive', 'active', 'suspended')
	primary = 'email'
	
	name = db.StringField()
	username = db.StringField(unique=True, required=True)
	email = db.EmailField(unique=True, required=True)
	password = db.StringField(required=True)
	status = db.StringField(choices=statuses, default='active')  # change to inactive
	
	
class Session(Document):
	# Idea: Each time a token is used, send a new access token back to the client
	
	statuses = Document.choices('logged in', 'logged out')
	
	user = db.ReferenceField(User, required=True)
	access_token = db.StringField(required=True)
	
	
anonymous = User(email='an@nymo.us', username='an', password='@').save()