import urllib.request
from bs4 import BeautifulSoup

def search(query):

	print("START SEARCH")

	textToSearch = query
	query = urllib.parse.quote(textToSearch)
	print("START SEARCH")
	url = "https://www.youtube.com/results?search_query=" + query
	url="https://medium.com/refactoring-ui/7-practical-tips-for-cheating-at-design-40c736799886"
	print("START SEARCH")
	response = urllib.request.urlopen(url)
	print("START SEARCH")
	html = response.read()
	print("START SEARCH")
	soup = BeautifulSoup(html, 'html.parser')
	print("START SEARCH")
	for vid in soup.findAll(attrs={'class':'yt-uix-tile-link'}):
	    print('https://www.youtube.com' + vid['href'])

search("hello")

