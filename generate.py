import webapp2
import jinja2
import os
import logging
from google.appengine.ext import ndb
from google.appengine.api import users
from models.myuser import MyUser
from models.anagramString import AnagramStringsDB
import functions

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)

class Generate(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        user = users.get_current_user()
        action = self.request.get('button')
        if user == None:
            rendered_template = {
            'login_url' : users.create_login_url(self.request.uri)
            }
            template = JINJA_ENVIRONMENT.get_template('templates/mainpage_guest.html')
            self.response.write(template.render(rendered_template))
            return

        myuser_key = ndb.Key('MyUser', user.user_id())
        myuser = myuser_key.get()
        if myuser == None:
            myuser = MyUser(id=user.user_id())
            myuser.put()

        results_dict = {'logout_url' : users.create_logout_url(self.request.uri)}
        template = JINJA_ENVIRONMENT.get_template('templates/generate.html')
        rendered_template = template.render(results_dict)
        self.response.write(rendered_template)
