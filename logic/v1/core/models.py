from logic.v1.models import Document, db


class User(Document):
	
	statuses = Document.choices('inactive', 'active', 'suspended')
	
	name = db.StringField()
	username = db.StringField()
	email = db.EmailField()
	password = db.StringField()
	status = db.StringField(choices=statuses)
	
	
class Session(Document):
	# Idea: Each time a token is used, send a new access token back to the client
	
	statuses = Document.choices('logged in', 'logged out')
	
	user = db.ReferenceField(User, required=True)
	access_token = db.StringField(required=True)
	
	
anonymous = User(email='an@nymo.us').save()