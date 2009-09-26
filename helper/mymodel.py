from google.appengine.ext import db

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
        v = float(v)
      try:
        setattr(self, k, v)
      except:
        setattr(self, k, int(v))