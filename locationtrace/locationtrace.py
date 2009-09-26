#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import wsgiref.handlers

from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import webapp
from locationtrace.models import LocationTrace
import os
import logging

from helper.CustomHandler import CustomHandler

import datetime



class index(CustomHandler):
  def get(self):
    for (k,v) in self.request.GET.iteritems():
      logging.debug(k+","+str(v))
    
    #locations = LocationTrace.all().order('timestamp').filter('user =', users.get_current_user()).fetch(1000)
    locations = LocationTrace.all().fetch(1000)
    
    template_values = {'locations':locations}
    CustomHandler.get(self, os.path.dirname(__file__), template_values)

    
class new(webapp.RequestHandler):
  def post(self):
    logging.debug("post new")

    lt = LocationTrace()
    
    lt.create(self.request.POST,{'user':users.get_current_user()})
    
    for (k,v) in self.request.POST.iteritems():
      logging.debug(k+","+str(v))

    lt.put()

    
class data(webapp.RequestHandler):
  def get(self,key):
    location = LocationTrace.get(key)
    if not location:
      return self.error(404)
    
    self.response.headers['Content-Type'] = 'audio/amr'
    self.response.out.write(location.location)

    
    #self.redirect('/sample/')



def main():
  application = webapp.WSGIApplication([('/locationtrace/new', new),
                                        ('/locationtrace/data/(.*)', data),
                                        ('/locationtrace', index)],
                                       debug=True)
  wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
  main()
