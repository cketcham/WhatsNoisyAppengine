from google.appengine.ext import db
from helper.mymodel import MyModel
import logging


class LocationTrace(MyModel):
  timestamp = db.DateTimeProperty()
  encodedPoints = db.StringProperty()
  encodedLevels = db.StringProperty()
  zoomFactor = db.IntegerProperty()
  numLevels = db.IntegerProperty()
  user = db.UserProperty()
