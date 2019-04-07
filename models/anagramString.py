from google.appengine.ext import ndb
class AnagramStringsDB(ndb.Model):
    stringVal  = ndb.StringProperty(repeated = True)
    sortedString = ndb.StringProperty()
    length = ndb.IntegerProperty()
    user_id = ndb.StringProperty()
    counter1 = ndb.IntegerProperty()
    counter2 = ndb.IntegerProperty()
