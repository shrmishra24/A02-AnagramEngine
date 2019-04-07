import webapp2
from webapp2 import Route

app = webapp2.WSGIApplication([
    Route('/', handler = 'home.HomePage'),
    Route('/add', handler = 'main.MainPage'),
    Route('/crud', handler = 'main.AnagramHandler'),
    Route('/search', handler = 'search.SearchHandler'),
    Route('/searchResult', handler = 'searchResults.SearchResult'),
    Route('/generate', handler = 'generate.Generate'),
    Route('/generateResult', handler = 'generateResult.GenerateHandler'),
],debug=True)
