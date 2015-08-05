from app.v1.models import Document, db


class User(Document):
	
	name = db.StringField()
	username = db.StringField()
	email = db.EmailField()
	password = db.StringField()