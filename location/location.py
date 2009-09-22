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
from location.models import Location
import os
import logging
from google.appengine.ext.webapp import template

import xml.dom.minidom
from django.utils import simplejson
from helper.glineenc import encode_locations

import datetime

class CustomHandler(webapp.RequestHandler):
  def get(self,template_values,template_name = None):
    if template_name == None:
      template_name = 'view/' + str(self.__class__.__name__)  + '.html'
    path = os.path.join(os.path.dirname(__file__), template_name)
    self.response.out.write(template.render(path, template_values)) 

class index(CustomHandler):
  def get(self):
    for (k,v) in self.request.GET.iteritems():
      logging.debug(k+","+str(v))
    
    amount = int(self.request.GET['amount'])
    offset = int(self.request.GET['offset'])
    
    locations = Location.all().order('timestamp').fetch(amount,offset)
    
    
    template_values = {'locations':locations, 'encoded':encode_locations(locations)}
    CustomHandler.get(self, template_values)

    
class new(webapp.RequestHandler):
  def post(self):
    locations = []
    
    if(self.request.params.has_key('data_string')):

      dom = xml.dom.minidom.parseString(self.request.params['data_string'])
      rows = dom.getElementsByTagName("row")
      for row in rows:
        fields = row.getElementsByTagName("field")
        for field in fields:

          if(field.attributes['name'].value == "location"):
            location_data = simplejson.loads(field.firstChild.data)

            logging.debug(location_data)

            for l in location_data:
              location = Location()
              location.location = db.GeoPt(str(l['latitude']) + "," + str(l['longitude']))
              location.timestamp = datetime.datetime.fromtimestamp(l["time"]/1000)
              location.user = users.get_current_user()
              
              locations += [location]
              
      #for location in locations:
      #  logging.debug(location.timestamp)
              
      db.put(locations)      

#    sample.create(self.request.POST,{'user':users.get_current_user()})
    
    for (k,v) in self.request.POST.iteritems():
      logging.debug(k+","+str(v))

#    sample.put()
    
class data(webapp.RequestHandler):
  def get(self,key):
    location = Location.get(key)
    if not location:
      return self.error(404)
    
    self.response.headers['Content-Type'] = 'audio/amr'
    self.response.out.write(location.location)

    
    #self.redirect('/sample/')



def main():
  application = webapp.WSGIApplication([('/location/new', new),
                                        ('/location/data/(.*)', data),
                                        ('/location', index)],
                                       debug=True)
  wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
  main()
