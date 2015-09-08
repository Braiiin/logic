from logic.v1.models import Document, db
from logic.v1 import User

class Service(Document):
    """represents a Braiiin service"""

    statuses = Document.choices(
        'private beta',
        'public beta',
        'launch',
        'legacy'
    )

    name = db.StringField()
    status = db.StringField(choices=statuses)


class Token(Document):
    """used for service and employment verification"""

    key = db.StringField()
    service = db.ReferenceField(Service)
    preset = db.DictField()


class Employment(Document):
    """represents a user's affiliation with a service"""

    statuses = Document.choices(
        'not approved',
        'approved',
        'suspended'
    )

    user = db.ReferenceField(User)
    service = db.ReferenceField(Service)
    status = db.StringField(choices=statuses)
    privilege = db.StringField(default='user')
    position = db.StringField(default='user')
