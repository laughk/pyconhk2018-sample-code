import os

from peewee import (
    SqliteDatabase,
    Model,
    CharField,
    TextField,
)

db = SqliteDatabase(os.path.join(os.path.dirname(__file__), 'bot_database.db'))


class Memo(Model):
    name = CharField(primary_key=True)
    text = TextField()

    class Meta:
        database = db


db.connect()
db.create_tables([Memo], safe=True)
