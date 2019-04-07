from google.appengine.ext import ndb
from google.appengine.api import users
from models.myuser import MyUser
from models.anagramString import AnagramStringsDB
from itertools import permutations
import re
import logging


with open("dictionary.txt") as word_file:  # NLTK dictionary downloaded for the lists of possible english words
    englishWords = set(word.strip().lower() for word in word_file)


# sorting of the entered word
def sorting(word):
    key = word.lower()
    return ''.join(sorted(key))

def add_anagram_if_exists(stringVal,anagram_key):
    anagramDB = anagram_key.get()
    if stringVal not in anagramDB.stringVal:
        anagramDB.stringVal.append(stringVal)
        anagramDB.counter1 = anagramDB.counter1+1
        anagramDB.put()


def add_new_anagram(stringVal, anagram_id, anagram_key, myuser):
    anagramDB = AnagramStringsDB(id=anagram_id)
    anagramDB.stringVal.append(stringVal)
    anagramDB.sortedString = sorting(stringVal)
    anagramDB.length = len(stringVal)
    anagramDB.user_id = myuser.key.id()
    anagramDB.counter1 = anagramDB.counter1+1
    anagramDB.put()


def getUserAnagrams(myuser):
    if myuser:
        result = []
        for anagram in myuser.userAnagramString:
            userAnagramString = anagram.get()
            result.append(userAnagramString)
        return result

def search_input_text(word):
    result = word.lower()
    result = re.sub('[^a-z]+', '', result) # accepting only alphabets for search values
    return result

def searchAnagram(self, word, myuser):
    anagram_id = myuser.key.id() + '/' + sorting(word) #appending the user key with sorted anagram
    anagram_key = ndb.Key(AnagramStringsDB, anagram_id)
    userAnagramString = anagram_key.get()
    if userAnagramString:
        result = userAnagramString.stringVal
        result.remove(word)
        return result
    else:
        return None

def allPermutations(word):
     # Get all permutations of string passed
     # permList = permutations(word)
     result = []
     output = []

     for text in xrange(1, len(word)+1):
         for item in permutations(word, text):
             result.append(''.join(item))
     for x in result:
         if len(x)>2:
             if x in englishWords:
                 if x not in output:
                     output.append(x)
     return output

def store_sub_anagrams_key_exists(stringVal, anagram_id, anagram_key, myuser):
    subAnagram = allPermutations(stringVal)
    # subAnagram.append(allPermutations(stringVal))
    anagramDB = anagram_key.get()
    for x in subAnagram:
        print("------------------00")
        logging.debug(x)
        if x not in anagramDB.stringVal:
            anagramDB.stringVal.append(x)
            anagramDB.counter1 = anagramDB.counter1+1
            anagramDB.put()

def store_sub_anagrams_no_key_exists(stringVal, anagram_id, anagram_key, myuser):
    subAnagram = allPermutations(stringVal)
    # subAnagram.append(allPermutations(stringVal))
    for x in subAnagram:
        anagramDB = AnagramStringsDB(id=anagram_id)
        anagramDB.stringVal.append(x)
        anagramDB.sortedString = sorting(stringVal)
        anagramDB.length = len(stringVal)
        anagramDB.user_id = myuser.key.id()
        anagramDB.counter1 = anagramDB.counter1+1
        anagramDB.put()
