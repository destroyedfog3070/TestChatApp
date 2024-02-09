from mongoengine import Document, StringField, DateTimeField
from datetime import datetime

class ChatEntry(Document):
    timestamp = DateTimeField(default=datetime.utcnow)
    user = StringField()
    message = StringField()



