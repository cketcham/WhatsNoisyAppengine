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

from google.appengine.api import users
from google.appengine.ext import webapp
from sample.models import Sample
import os
import logging
from google.appengine.ext.webapp import template
from helper.CustomHandler import CustomHandler

class index(CustomHandler):
  def get(self):
    for (k,v) in self.request.GET.iteritems():
      logging.debug(k+","+str(v))

    user = users.get_current_user()

    #display all the samples if the user isn't logged in or is admin
    if not user or users.is_current_user_admin():
      cool = Sample.all().filter("type = ", "cool").fetch(10)
      noisy = Sample.all().filter("type = ", "noisy").fetch(10)
    else:
      cool = Sample.all().filter("user = ", user).filter("type = ", "cool").fetch(10)
      noisy = Sample.all().filter("user = ", user).filter("type = ", "noisy").fetch(10)
        

    template_values = {'cool':cool, 'noisy':noisy}
    CustomHandler.get(self, os.path.dirname(__file__), template_values)

    
class new(webapp.RequestHandler):
  def post(self):
    logging.debug("post new")

    sample = Sample()
    
    sample.create(self.request.POST,{'user':users.get_current_user()})
    
    for (k,v) in self.request.POST.iteritems():
      logging.debug(k+","+str(v))

    sample.put()
    
class data(webapp.RequestHandler):
  def get(self,key):
    sample = Sample.get(key)
    if not sample:
      return self.error(404)
    
    self.response.headers['Content-Type'] = 'audio/amr'
    self.response.out.write(sample.file)

    
    #self.redirect('/sample/')



def main():
  application = webapp.WSGIApplication([('/sample/new', new),
                                        ('/sample/data/(.*)', data),
                                        ('/sample', index)],
                                       debug=True)
  wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
  main()
