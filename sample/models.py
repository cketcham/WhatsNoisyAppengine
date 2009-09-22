from google.appengine.ext import db
import logging


class MyModel(db.Model):
  def create(self, params, extra):
    params.update(extra)
    for (k,v) in params.iteritems():
      if k == "location":
        v = v.split(',')
        v = db.GeoPt(v[0],v[1])
      elif k == "file":
        v = db.Blob(v.file.read())
      setattr(self, k, v)

class Sample(MyModel):
  title = db.StringProperty()
  type = db.StringProperty()
  file = db.BlobProperty()
  location = db.GeoPtProperty()
  user = db.UserProperty()
