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

class GenerateHandler(webapp2.RequestHandler):
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


        if action == 'Generate':

            searchVal = functions.search_input_text(self.request.get('searchVal'))
            user = users.get_current_user()
            myuser_key = ndb.Key('MyUser', user.user_id())
            myuser = myuser_key.get()

            search_result= functions.allPermutations(searchVal)


            results_dict = {'search_result' : search_result,
                            'searchVal' : searchVal.upper(),
                            'logout_url' : users.create_logout_url(self.request.uri)}



            template = JINJA_ENVIRONMENT.get_template('templates/generateResult.html')
            rendered_template = template.render(results_dict)
            self.response.write(rendered_template)

    def post(self):
        action = self.request.get('button')
        if action =='Add':
            stringVal = self.request.get('searchVal')
            stringVal = stringVal.lower()
            user = users.get_current_user()
            myuser_key = ndb.Key('MyUser', user.user_id())
            myuser = myuser_key.get()


            anagram_id = myuser.key.id() + '/' + functions.sorting(stringVal) #appending the user key with sorted anagram
            anagram_key = ndb.Key(AnagramStringsDB, anagram_id)
            userAnagramString = anagram_key.get()
            # if the sorted anagram word already exists then it will append with the string.
            if userAnagramString:
                functions.store_sub_anagrams_key_exists(stringVal, anagram_id, anagram_key, myuser)

            # if the word does not exists then new entry will be done.
            else:
                functions.store_sub_anagrams_no_key_exists(stringVal,anagram_id,anagram_key,myuser)
                 # add key of the new anagram to the users KeyProperty
                myuser.userAnagramString.append(anagram_key)
                myuser.put()

                functions.store_sub_anagrams_key_exists(stringVal, anagram_id, anagram_key, myuser)
        self.redirect('/generateResult?searchVal='+stringVal+'&button=Generate')
