from google.appengine.api import users
from google.appengine.ext import webapp
import os
import logging
from google.appengine.ext.webapp import template

class CustomHandler(webapp.RequestHandler):
  def get(self,file,template_values = {},template_name = None):
    if template_name == None:
      template_name = 'view/' + str(self.__class__.__name__)  + '.html'
      
    user = users.get_current_user()

    if user:
      login_text = 'Sign Out'
      login_url = users.create_logout_url(self.request.uri)
    else:
      login_text = 'Sign In'
      login_url = users.create_login_url(self.request.uri)

    template_values.update({'login_url':login_url ,'login_text':login_text, 'user':user })
    path = os.path.join(file, template_name)
    self.response.out.write(template.render(path, template_values)) 
