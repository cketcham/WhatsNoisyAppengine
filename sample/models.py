from google.appengine.ext import db
from helper.mymodel import MyModel
import logging




class Sample(MyModel):
  title = db.StringProperty()
  type = db.StringProperty()
  file = db.BlobProperty()
  location = db.GeoPtProperty()
  user = db.UserProperty()
  timestamp = db.DateTimeProperty()
