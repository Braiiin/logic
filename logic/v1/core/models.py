from logic.v1.models import Document, db


class User(Document):
	
	statuses = Document.choices('inactive', 'active', 'suspended')
	primary = 'email'
	
	name = db.StringField()
	username = db.StringField(required=True)
	email = db.EmailField(unique_with='username', required=True)
	password = db.StringField(required=True)
	salt = db.StringField()
	status = db.StringField(choices=statuses, default='active')  # change to inactive
	
	
class Session(Document):
	# Idea: Each time a token is used, send a new access token and/or nonce 
	#  back to the client - REMEMBER: nonce cannot be overridden (else
	# middle men can post password hash against logic tier
	
	statuses = Document.choices('logged in', 'logged out')
	
	user = db.ReferenceField(User, required=True)
	access_token = db.StringField(required=True)
	nonce = db.StringField(required=True)
	destroyed_at = db.DateTimeField(default=None)
	
	
anonymous = User(
	email='an@nymo.us', 
	username='an', 
	password='@'
).get_or_create()