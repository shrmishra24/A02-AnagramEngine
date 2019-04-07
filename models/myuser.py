from google.appengine.ext import ndb
from anagramString import AnagramStringsDB
class MyUser(ndb.Model):
    userAnagramString =  ndb.KeyProperty(kind= AnagramStringsDB, repeated= True)
