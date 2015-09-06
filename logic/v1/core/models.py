from logic.v1.models import Document, db
from logic.v1.exceptions import EmailError

class User(Document):

    statuses = Document.choices('inactive', 'active', 'suspended')
    primary = 'email'

    name = db.StringField()
    username = db.StringField(required=True)
    email = db.EmailField(unique_with='username', required=True)
    password = db.StringField(required=True)
    salt = db.StringField()
    status = db.StringField(choices=statuses, default='active')


class Session(Document):

    statuses = Document.choices('logged in', 'logged out')

    user = db.ReferenceField(User, required=True)
    access_token = db.StringField(required=True)
    destroyed_at = db.DateTimeField(default=None)


class Email(Document):

    statuses = Document.choices('drafted', 'sent')

    sender = db.StringField(required=True, default='no-reply@braiiin.com')
    to = db.StringField(required=True),
    subject = db.StringField(required=True)
    html = db.StringField(),
    body = db.StringField(),
    status = db.StringField(choices=statuses)

    def send(self, **overrides):
        """Sends the email"""
        self.load(**overrides)

        try:
            message = Message(From=self.sender, To=self.to, charset="utf-8")
            message.Subject = self.subject
            message.Html = self.html
            message.Body = self.body

            sender = Mailer('smtp.braiiin.com')
            sender.send(message)
        except AttributeError:
            raise EmailError('Missing one of required attributes: %s' % str([
                'from', 'to', 'html', 'body', 'subject']))


anonymous = User(
    email='an@nymo.us',
    username='an',
    password='@'
).get_or_create()
