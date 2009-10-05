from google.appengine.ext import db
import datetime

class MyModel(db.Model):
  def create(self, params, extra):
    params.update(extra)
    for (k,v) in params.iteritems():
      if k == "location":
        v = v.split(',')
        v = db.GeoPt(v[0],v[1])
      elif k == "file":
        v = db.Blob(v.file.read())
      elif k == "timestamp":
        v = datetime.datetime.fromtimestamp(float(v)/1000)
      try:
        setattr(self, k, v)
      except:
        setattr(self, k, int(v))