from google.appengine.ext import db
import logging


class Location(db.Model):
  timestamp = db.DateTimeProperty()
  location = db.GeoPtProperty()
  user = db.UserProperty()
